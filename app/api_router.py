from fastapi import APIRouter

from app.domains.user.endpoints import user_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["User"])