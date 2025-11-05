from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class LinkCreate(BaseModel):
    """Schema for creating a new short link."""
    original_url: HttpUrl = Field(..., description="Original URL to shorten")


class LinkRead(LinkCreate):
    """Schema for reading link data with analytics."""
    id: UUID = Field(..., description="Unique identifier for the link")
    short_url: str | None = Field(None, description="Shortened URL code")
    click_count: int = Field(0, description="Number of clicks on this link")
    created_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the link was created",
    )

    model_config = ConfigDict(from_attributes=True)
