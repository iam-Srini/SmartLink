from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from uuid import UUID
from datetime import datetime, timezone

class LinkCreate(BaseModel):
    original_url : HttpUrl = Field(..., description="Original Url")

class LinkRead(LinkCreate):
    id: UUID = Field(..., description="Link Id")
    short_url: str = Field(None, description="Shortened URL")
    clicks: int = Field(0, description="Number of clicks (for analytics)")
    created_date: datetime= Field(default_factory=lambda: datetime.now(timezone.utc), description="link created at")
    
    model_config = ConfigDict(from_attributes= True)

    