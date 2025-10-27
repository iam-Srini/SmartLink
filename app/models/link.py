from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy import String, INTEGER, DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime, timezone

class Link(Base):
    __tablename__ = "links"

    id : Mapped[str] = mapped_column(String(36), primary_key= True, default= lambda : str(uuid4()),nullable=False)
    original_url : Mapped[str] = mapped_column(String(2048))
    short_url : Mapped[str] = mapped_column(String(10), index=True, unique=True, nullable=False)
    click_count: Mapped[int] = mapped_column(INTEGER, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default= datetime.now(timezone.utc), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36),ForeignKey("users.id"),nullable=True)
    
    user: Mapped["User"] = relationship("User",back_populates="links")
    clicks: Mapped[list["ClickLog"]] = relationship("ClickLog", back_populates="link", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Link(id = {self.id}, short_url = {self.short_url}, clicks = {self.clicks})>"
