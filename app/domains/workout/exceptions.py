from starlette import status

from app.common.exception import CustomException


class WorkoutNotFound(CustomException):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "존재하지 않는 운동 기록입니다."