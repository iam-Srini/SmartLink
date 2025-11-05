from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserBase(BaseModel):
    """Base schema for user shared fields."""
    email: EmailStr = Field(..., max_length=100, description="The email of the user")


class UserCreate(UserBase):
    """Schema for creating a new user with password validation."""
    username: str = Field(..., max_length=30, description="The name of the user")
    password: str = Field(..., min_length=8, max_length=20, description="The password of the user")

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Ensure password meets complexity requirements."""
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in value):
            raise ValueError("Password must contain at least one special character.")
        return value


class UserRead(UserBase):
    """Schema for reading user data."""
    id: str
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Schema for updating a user. All fields are optional.
    Password validation applies if a new password is provided.
    """
    username: str | None = Field(None, max_length=30, description="The name of the user")
    email: EmailStr | None = Field(None, max_length=100, description="The email of the user")
    password: str | None = Field(None, min_length=8, max_length=20, description="The password of the user")

    @field_validator("password")
    def validate_password(cls, value: str | None) -> str | None:
        """Ensure password meets complexity requirements if provided."""
        if value is not None:
            if not any(char.isdigit() for char in value):
                raise ValueError("Password must contain at least one digit.")
            if not any(char.isupper() for char in value):
                raise ValueError("Password must contain at least one uppercase letter.")
            if not any(char.islower() for char in value):
                raise ValueError("Password must contain at least one lowercase letter.")
            if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in value):
                raise ValueError("Password must contain at least one special character.")
        return value


class UserLogin(UserBase):
    """Schema for user login credentials."""
    password: str = Field(..., min_length=8, max_length=20, description="The password of the user")
