from fastapi import APIRouter

from app.domains.auth.endpoints import auth_router
from app.domains.comment.endpoints import comment_router
from app.domains.post.endpoints import post_router
from app.domains.user.endpoints import user_router
from app.domains.workout.endpoints import workout_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(post_router, prefix="/posts", tags=["Post"])
router.include_router(comment_router, prefix="/posts/{post_id}/comments", tags=["Comment"])
router.include_router(workout_router, prefix="/workouts", tags=["Workout"])