from typing import List

from fastapi import APIRouter, Depends, Form, UploadFile, File

from app.common.response import BaseResponse
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.workout.schemas import *
from app.domains.workout.service import *
from database.session import get_db

workout_router = APIRouter()


@workout_router.get("", response_model=BaseResponse[GroupedWorkoutDTO])
async def get_workouts(
        month: str,
        db=Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 운동 목록 조회
    ### Query Parameters
    - month: YYYY-MM 형식의 날짜
    ### Response
    - 200: BaseResponse
    - 401: 인증 실패
    """

    workouts = await get_workout_list(
        db=db,
        user_id=user.sub,
        month=month,
    )

    return BaseResponse(message="운동 목록을 조회했습니다.", data=workouts)

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

@workout_router.delete("/{workout_id}", response_model=BaseResponse[BaseWorkoutDTO])
async def delete_workout_id(
        workout_id: str,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 운동 일지 삭제
    ### Response
    - 204: BaseResponse
    - 401: 인증 실패
    """
    await check_workout_authorization(db=db, workout_id=workout_id, user_id=user.sub)
    await delete_workout(db=db, workout_id=workout_id)

    return BaseResponse(message="운동을 삭제했습니다.")