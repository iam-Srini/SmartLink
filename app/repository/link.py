from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request

from app.schemas.link import LinkCreate
from app.core.utils import generate_short_code_from_uuid
from app.models.link import Link
from app.models.user import User
from app.models.click_log import ClickLog


class LinkRepository:
    """
    Repository class for managing link creation, redirection, and analytics.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_link(self, data: LinkCreate, user_data: User) -> Link:
        """
        Create a new shortened link for a given user.
        """
        short_link = generate_short_code_from_uuid(data.original_url)
        while self.db.query(Link).filter(Link.short_url == short_link).first():
            short_link = generate_short_code_from_uuid(data.original_url)

        new_link = Link(
            original_url=str(data.original_url),
            short_url=short_link,
            user_id=user_data.id,
        )
        self.db.add(new_link)
        self.db.commit()
        self.db.refresh(new_link)
        return new_link

    def redirect_link(self, request: Request, short_url: str) -> str:
        """
        Handle link redirection, increment click count, and log click data.
        """
        link = self.db.query(Link).filter(Link.short_url == short_url).first()
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found",
            )

        link.click_count += 1
        self.db.commit()
        self.db.refresh(link)

        log = ClickLog(
            link_id=link.id,
            referrer=request.headers.get("referrer"),
            user_agent=request.headers.get("user_agent"),
            ip_address=request.client.host,
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        print(f"Redirecting to original URL: {link.original_url}")
        return link.original_url

    def get_all_urls(self, user_data: User) -> list[Link]:
        """
        Retrieve all links created by a specific user.
        """
        return self.db.query(Link).filter(Link.user_id == user_data.id).all()

    def get_link_stats(self, user_data: User, short_url: str) -> dict:
        """
        Retrieve analytics data (click stats and recent clicks) for a specific link.
        """
        link = (
            self.db.query(Link)
            .filter(Link.short_url == short_url, Link.user_id == user_data.id)
            .first()
        )
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Link not found",
            )

        logs = self.db.query(ClickLog).filter(ClickLog.link_id == link.id).all()

        return {
            "original_url": link.original_url,
            "short_code": link.short_url,
            "clicks_count": link.click_count,
            "created_at": link.created_at,
            "recent_clicks": [
                {
                    "timestamp": log.timestamp,
                    "user_agent": log.user_agent,
                    "referrer": log.referrer,
                    "ip": log.ip_address,
                }
                for log in logs[-10:]
            ],
        }
