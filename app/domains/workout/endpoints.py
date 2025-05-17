from typing import List

from fastapi import APIRouter, Depends, Form, UploadFile, File

from app.common.response import BaseResponse
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.workout.schemas import *
from app.domains.workout.service import *
from database.session import get_db

workout_router = APIRouter()

@workout_router.post("", response_model=BaseResponse[BaseWorkoutDTO])
async def post_workout(
        workout: CreateWorkoutDTO,
        db=Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 운동 등록
    ### Request Body
    - workout_date: date
    - start: time
    - end: time
    - title: str
    - content: str
    - color: str
    ### Response
    - 201: BaseResponse
    - 400: 필수 필드 누락
    - 401: 인증 실패
    """

    workout_id = await create_workout(
        db=db,
        workout=workout,
        user_id=user.sub,
    )

    return BaseResponse(message="운동을 등록했습니다.", data={
        "workout_id": workout_id
    })