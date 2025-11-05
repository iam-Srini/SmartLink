import uuid
from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ClickLog(Base):
    """
    ORM model for tracking individual link clicks with metadata.
    """
    __tablename__ = "click_log"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
    link_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("links.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
    )
    referrer: Mapped[str] = mapped_column(String(2048), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)

    link: Mapped["Link"] = relationship("Link", back_populates="clicks")

    def __repr__(self) -> str:
        return (
            f"<ClickLog(link_id={self.link_id}, ip={self.ip_address}, "
            f"at={self.timestamp})>"
        )
