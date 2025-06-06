import logging
import uuid
from collections import defaultdict
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.auth.exceptions import NotAuthorization
from app.domains.files.service import save_photo_list, delete_photo_lists, change_photo_list, get_photo_list
from app.domains.workout.exceptions import WorkoutNotFound
from app.domains.workout.models import Workout
from app.domains.workout.repository import WorkoutRepository
from app.domains.workout.schemas import CreateWorkoutDTO


async def check_workout_authorization(
        *, db: AsyncSession, workout_id: str, user_id: str
):
    workout_repo = WorkoutRepository(db=db)

    workout = await workout_repo.get(workout_id=workout_id)
    if not workout:
        raise WorkoutNotFound()
    if workout.user_id != user_id:
        raise NotAuthorization()

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
            "workout_id": workout.workout_id,
            "time": f"{workout.start.strftime('%H:%M')}–{workout.end.strftime('%H:%M')}",
            "title": workout.title,
            "content": workout.content,
            "color": workout.color,
            "image_url": await get_photo_list(db=db, target_id=workout.workout_id),
        })

    return response

async def update_workout(
        *, db: AsyncSession, workout_id: str, updated_workout: CreateWorkoutDTO
):
    workout_repo = WorkoutRepository(db=db)

    workout = await workout_repo.get(workout_id=workout_id)
    if not workout:
        raise WorkoutNotFound()

    workout.workout_date = updated_workout.date
    workout.start = updated_workout.start
    workout.end = updated_workout.end
    workout.title = updated_workout.title
    workout.content = updated_workout.content
    workout.color = updated_workout.color

    try:
        await change_photo_list(db=db, urls=updated_workout.image_url, target_id=workout_id, type="workout")
        await db.commit()
        return workout_id
    except Exception as e:
        logging.error(e)
        raise DBException()

async def delete_workout(*, db: AsyncSession, workout_id: str):
    workout_repo = WorkoutRepository(db=db)

    workout = await workout_repo.get(workout_id=workout_id)
    if not workout:
        raise WorkoutNotFound()

    try:
        await workout_repo.delete(workout_id=workout_id)
        await delete_photo_lists(db=db, target_id=workout_id)
    except Exception as e:
        logging.error(e)
        raise DBException()

async def delete_workout_for_user_id(*, db: AsyncSession, user_id: str):
    workout_repo = WorkoutRepository(db=db)

    try:
        workouts = await workout_repo.get_by_user_id(user_id=user_id)
        for workout in workouts:
            await workout_repo.delete(workout_id=workout.workout_id)
            await delete_photo_lists(db=db, target_id=workout.workout_id)
    except Exception as e:
        logging.error(e)
        raise DBException()