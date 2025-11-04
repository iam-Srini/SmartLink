from fastapi import APIRouter, Depends
from app.schemas.user import UserRead, UserCreate
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.repository.users import UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.email_utils import send_otp_email
from fastapi import BackgroundTasks

user_router = APIRouter(prefix="/users")

@user_router.post(
    path="/register",
    response_model= UserRead,
    description="User Registration")
def user_register( user_create: UserCreate, background_tasks:BackgroundTasks, db: Session = Depends(get_db)):
    user_repo = UserRepository(db=db)
    new_user = user_repo.user_register_repo(user_create)
    send_otp_email(background_tasks, new_user.email, new_user.otp_code)
    return new_user

@user_router.post(
    path="/verify-email",
    description="User Verification"
)
def verify_user(email: str, otp: str, db: Session = Depends(get_db)):
    user_repo = UserRepository(db= db)
    return user_repo.verify_user_repo(email= email, otp=otp)

@user_router.post(
    path = "/login",
    description="login page"
    )   
def user_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"inside router")
    user_repo = UserRepository(db = db)
    access_token =  user_repo.login_user_repo(email=request.username,password=request.password)
    print(f"access_token:{access_token}")
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post(
    path = "/otp-request",
    description="Request a new OTP in case of expiry or not received"
)
def user_request_otp(email: str, background_tasks:BackgroundTasks, db : Session = Depends(get_db)):
    user_repo = UserRepository(db=db)
    user = user_repo.request_otp(user_email=email)
    send_otp_email(background_tasks, user.email, user.otp_code)
    return {"message": "OTP sent successfully", "email": user.email}
