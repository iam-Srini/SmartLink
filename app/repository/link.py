from sqlalchemy.orm import session
from app.schemas.link import LinkCreate
from app.core.utils import generate_short_code_from_uuid
from app.models.link import Link
from fastapi import HTTPException, status



class LinkRepository:
    def __init__(self, db:session):
        self.db = db
    
    def create_link(self, data:LinkCreate):
        short_link = generate_short_code_from_uuid(data.original_url)
        while self.db.query(Link).filter(Link.short_url == short_link).first():
            short_link = generate_short_code_from_uuid(data.original_url)
        new_link = Link(
            original_url = data.original_url,
            short_url = short_link
        )
        self.db.add(new_link)
        self.db.commit()
        self.refresh(new_link)
        return new_link
    
    def redirect_link(self, short_url:str):
        link = self.db.query(Link).filter(Link.short_url == short_url).first()
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found"
            )
        link.clicks += 1
        session.add(link)
        session.commit()
        return link.original_url
        
        


