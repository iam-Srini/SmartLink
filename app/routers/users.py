from fastapi import APIRouter, Depends
from app.schemas.user import UserRead, UserCreate
from app.db.session import get_db
from sqlalchemy.orm import session
from app.repository.users import UserRepository
from app.schemas.token import TokenData
from fastapi.security import OAuth2PasswordRequestForm


user_router = APIRouter(prefix="/users")

@user_router.post(
    path="/register",
    response_model= UserRead,
    description="User Registration")
def user_register( user_create: UserCreate, Session: session = Depends(get_db)):
    user_repo = UserRepository(db=Session)
    return user_repo.user_register_repo(user_create)

@user_router.post(
    path="/verify-email",
    description="User Verification"
)
def verify_user(email: str, otp: str, Session: session = Depends(get_db)):
    user_repo = UserRepository(db= Session)
    return user_repo.verify_user_repo(email= email, otp=otp)

@user_router.post(
    path = "/login",
    description="login page"
    )   
def user_login(request: OAuth2PasswordRequestForm = Depends(), Session = Depends(get_db)):
    print(f"inside router")
    user_repo = UserRepository(db = Session)
    access_token =  user_repo.login_user_repo(email=request.username,password=request.password)
    print(f"access_token:{access_token}")
    return {"access_token": access_token, "token_type": "bearer"}





    