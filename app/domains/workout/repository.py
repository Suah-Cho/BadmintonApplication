from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from app.domains.workout.models import Workout


class WorkoutRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: str, month: str):
        result = await self.db.execute(
            select(Workout)
            .options(selectinload(Workout.photos))
            .where(
                Workout.user_id == user_id,
                Workout.workout_date.like(f"{month}%")
            )
        )
        return result.scalars().all()

    async def create(self, workout: Workout):
        self.db.add(workout)
        return workout