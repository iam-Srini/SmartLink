"""
Repository layer for handling database CRUD operations.
"""

from .users import UserRepository
from .link import LinkRepository

__all__ = ["UserRepository", "LinkRepository"]
