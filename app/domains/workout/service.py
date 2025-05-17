import logging
import uuid
from collections import defaultdict
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

async def get_workout_list(
        *, db: AsyncSession, user_id: str, month: str
):
    workout_repo = WorkoutRepository(db=db)

    rows = await workout_repo.get_all(user_id=user_id, month=month)

    response = defaultdict(list)
    for workout in rows:
        date = str(workout.workout_date)
        response[date].append({
            "time": f"{workout.start.strftime('%H:%M')}–{workout.end.strftime('%H:%M')}",
            "title": workout.title,
            "content": workout.content,
            "color": workout.color,
            "image_url": [photo.url for photo in workout.photos],
        })

    return response