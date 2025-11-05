"""
Database models for SmartLink.
"""

from .base import Base
from .user import User
from .link import Link
from .click_log import ClickLog

__all__ = ["Base", "User", "Link", "ClickLog"]
