from routers.link import link_router
from routers.users import user_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(link_router)
router.include_router(user_router)