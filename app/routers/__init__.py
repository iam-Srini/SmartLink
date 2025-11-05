from fastapi import APIRouter
from .link import link_router
from .users import user_router

# Initialize main API router
router = APIRouter()

# Include feature-specific routers
router.include_router(user_router)
router.include_router(link_router)
