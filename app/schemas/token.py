from pydantic import BaseModel, EmailStr, Field


class TokenData(BaseModel):
    """Schema representing user login credentials."""
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="User password")
