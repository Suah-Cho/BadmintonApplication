from fastapi import APIRouter

from app.domains.auth.endpoints import auth_router
from app.domains.post.endpoints import post_router
from app.domains.user.endpoints import user_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(post_router, prefix="/posts", tags=["Post"])