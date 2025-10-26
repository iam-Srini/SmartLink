from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from .auth_handler import verify_access_token
from app.models.user import User
from app.repository.users import UserRepository

auth_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token : str = Depends(auth_bearer), db:Session = Depends(get_db))->User:
    try:
        print(f"token : {token}")
        token_data = verify_access_token(token)
        print(f"Token data:{token_data}")
        user_repo = UserRepository(db)
        return user_repo.get_user_by_id(token_data)
    
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or Expired Token"
        )
    