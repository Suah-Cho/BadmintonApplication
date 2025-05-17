import logging
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.photo.service import save_photo_list
from app.domains.workout.models import Workout
from app.domains.workout.repository import WorkoutRepository
from app.domains.workout.schemas import CreateWorkoutDTO


async def create_workout(
        *, db: AsyncSession, workout: CreateWorkoutDTO, user_id: str
):
    workout_repo = WorkoutRepository(db=db)

    new_workout = Workout(
        workout_id=str(uuid.uuid4()),
        user_id=user_id,
        workout_date=workout.date,
        start=workout.start,
        end=workout.end,
        title=workout.title,
        content=workout.content,
        color=workout.color,
        create_ts=datetime.now(),
    )

    try:
        async with db.begin():
            await save_photo_list(urls=workout.image_url, target_id=new_workout.workout_id, type="workout", db=db)
            await workout_repo.create(workout=new_workout)
    except Exception as e:
        logging.error(e)
        raise DBException()

    return new_workout.workout_id