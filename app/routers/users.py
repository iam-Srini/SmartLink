from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserRead, UserCreate
from app.db.session import get_db
from app.repository import UserRepository
from app.auth.email_utils import send_otp_email

# Router setup
user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(
    path="/register",
    response_model=UserRead,
    description="Register a new user and send OTP for verification.",
)
def user_register(
    user_create: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Register a new user and send an OTP email for verification."""
    user_repo = UserRepository(db=db)
    new_user = user_repo.user_register_repo(user_create)
    send_otp_email(background_tasks, new_user.email, new_user.otp_code)
    return new_user


@user_router.post(
    path="/verify-email",
    description="Verify user email address using the OTP.",
)
def verify_user(
    email: str,
    otp: str,
    db: Session = Depends(get_db),
):
    """Verify a user's email using a provided OTP."""
    user_repo = UserRepository(db=db)
    return user_repo.verify_user_repo(email=email, otp=otp)


@user_router.post(
    path="/login",
    description="Authenticate user and return an access token.",
)
def user_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate a verified user and return a JWT access token."""
    user_repo = UserRepository(db=db)
    access_token = user_repo.login_user_repo(
        email=request.username,
        password=request.password,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post(
    path="/otp-request",
    description="Request a new OTP if the previous one expired or was not received.",
)
def user_request_otp(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Request a new OTP for user email verification."""
    user_repo = UserRepository(db=db)
    user = user_repo.request_otp(user_email=email)
    send_otp_email(background_tasks, user.email, user.otp_code)
    return {"message": "OTP sent successfully", "email": user.email}
