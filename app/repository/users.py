from sqlalchemy.orm import session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.models.user import User
from app.auth.otp_utils import generate_otp, otp_expiry_time
from datetime import datetime, timezone
from app.auth.auth_handler import create_access_token


class UserRepository:
    def __init__(self, db: session):
        self.db = db

    def user_register_repo(self, user_create: UserCreate):
        new_user = User(
            username = user_create.username.strip(),
            email = user_create.email.lower(),
            password = user_create.password,
            otp_code = generate_otp(),
            otp_expiry = otp_expiry_time(),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def verify_user_repo(self, email: str, otp: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User Not Found."
            )
        if user.is_verified:
            return {"message": "User already verified"}
        if user.otp_code != otp:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP Code."
            )
        if user.otp_expiry.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="OTP Expired."
            )
        user.is_verified = True
        user.otp_code = None
        user.otp_expiry = None
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {"message": "User Verified Successfully."}
    
    def login_user_repo(self, email: str, password: str)-> dict:
        user = self.db.query(User).filter(User.email == email).first()
        if not user :
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Password"
            )
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is Not verified"
            )
        if user.password != password:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect Password"
            )
        access_token = create_access_token(
            {"sub":user.id}
        )
        return access_token
    
    def get_user_by_id(self, user_id:str):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )
        return user
    
    def request_otp(self, user_email: str):
        user = self.db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "No User found with the provided email"
            )
        if user.is_verified:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "User is already verified"
            )
        user.otp_code = generate_otp()
        user.otp_expiry = otp_expiry_time()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


        