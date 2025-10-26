from pydantic import BaseModel, EmailStr, Field


class TokenData(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="user password")
