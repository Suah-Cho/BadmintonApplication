from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.workout.models import Workout


class WorkoutRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, workout: Workout):
        self.db.add(workout)
        return workout