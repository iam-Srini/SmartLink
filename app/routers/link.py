from fastapi import APIRouter, Depends, status
from app.schemas.link import LinkRead
from app.repository.link import LinkRepository
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.link import LinkCreate
from fastapi.responses import RedirectResponse
from app.auth.auth_bearer import get_current_user
from app.models.user import User

link_router = APIRouter(prefix="/link", tags=["Links"])

@link_router.post("/", response_model=LinkRead)
def create_link(
    data: LinkCreate,
    session: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
    
):
    link_repo = LinkRepository(db = session)
    return link_repo.create_link(data = data, user_data= user_data)

@link_router.get("/{short_url}")
def redirect_link(
    short_url : str,
    session : Session = Depends(get_db)
):
    link_repo = LinkRepository(db = session)
    original_url = link_repo.redirect_link(short_url=short_url)
    return RedirectResponse(url=original_url, status_code= status.HTTP_307_TEMPORARY_REDIRECT)

@link_router.get("/all", response_model= list[LinkRead])
def get_user_links(
    session : Session = Depends(get_db),
    user_data: User = Depends(get_current_user)
):
    link_repo = LinkRepository(db=session)
    return link_repo.get_all_urls(user_data=user_data)
    
