from sqlalchemy.orm import session
from app.schemas.link import LinkCreate
from app.core.utils import generate_short_code_from_uuid
from app.models.link import Link
from fastapi import HTTPException, status
from app.models.user import User



class LinkRepository:
    def __init__(self, db:session):
        self.db = db
    
    def create_link(self, data:LinkCreate, user_data:User):

        short_link = generate_short_code_from_uuid(data.original_url)
        while self.db.query(Link).filter(Link.short_url == short_link).first():
            short_link = generate_short_code_from_uuid(data.original_url)
        new_link = Link(
            original_url = str(data.original_url),
            short_url = short_link,
            user_id = user_data.id
        )
        self.db.add(new_link)
        self.db.commit()
        return new_link
    
    def redirect_link(self, short_url:str):
        link = self.db.query(Link).filter(Link.short_url == short_url).first()
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found"
            )
        print(f"{link}")
        link.clicks += 1
        self.db.commit()
        self.db.refresh(link)
        print(link.clicks)
        print(link.original_url)
        return link.original_url
    
    def get_all_urls(self, user_data: User):
        links = self.db.query(Link).filter(Link.user_id == user_data.id).all()
        return links

        
        


