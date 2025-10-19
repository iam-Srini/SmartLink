from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime,Boolean
from datetime import datetime, timezone
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[str]= mapped_column(String(36), primary_key=True, default= lambda :str(uuid.uuid4()), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    otp_code: Mapped[str] = mapped_column(str(10),nullable=True)
    otp_expiry: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username}, created_at = {self.created_at})>"

