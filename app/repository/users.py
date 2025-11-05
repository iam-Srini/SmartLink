"""User repository with CRUD and authentication logic."""

from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.auth.otp_utils import generate_otp, otp_expiry_time
from app.auth.auth_handler import create_access_token


class UserRepository:
    """
    Repository class for handling user registration, verification,
    authentication, and OTP-related operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def user_register_repo(self, user_create: UserCreate) -> User:
        """
        Register a new user and generate OTP for email verification.
        """
        new_user = User(
            username=user_create.username.strip(),
            email=user_create.email.lower(),
            password=user_create.password,
            otp_code=generate_otp(),
            otp_expiry=otp_expiry_time(),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def verify_user_repo(self, email: str, otp: str) -> dict:
        """
        Verify user's email using the provided OTP.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        if user.is_verified:
            return {"message": "User already verified."}

        if user.otp_code != otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code.",
            )

        if user.otp_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired.",
            )

        user.is_verified = True
        user.otp_code = None
        user.otp_expiry = None
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {"message": "User verified successfully."}

    def login_user_repo(self, email: str, password: str) -> dict:
        """
        Authenticate a verified user and generate an access token.
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not verified.",
            )

        if user.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )

        access_token = create_access_token({"sub": user.id})
        return access_token

    def get_user_by_id(self, user_id: str) -> User:
        """
        Retrieve a user record by its ID.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    def request_otp(self, user_email: str) -> User:
        """
        Generate and resend OTP for unverified users.
        """
        user = self.db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user found with the provided email.",
            )

        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already verified.",
            )

        user.otp_code = generate_otp()
        user.otp_expiry = otp_expiry_time()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
