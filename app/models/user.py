import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    """
    ORM model representing a user in the system.
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    otp_code: Mapped[str] = mapped_column(String(6), nullable=True)
    otp_expiry: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    links: Mapped[list["Link"]] = relationship("Link", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, email={self.email}, "
            f"username={self.username}, created_at={self.created_at})>"
        )
