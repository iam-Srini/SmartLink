from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.repository.users import UserRepository
from .auth_handler import verify_access_token

auth_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: dict = Depends(auth_bearer),
    db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the currently authenticated user based on the provided access token.
    """
    try:
        print(f"Token: {token}")
        token_data = verify_access_token(token)
        print(f"Token data: {token_data}")
        user_repo = UserRepository(db)
        return user_repo.get_user_by_id(token_data)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired token"
        )
