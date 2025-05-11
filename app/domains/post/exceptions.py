from fastapi import status

from app.common.exception import CustomException


class PostNotFound(CustomException):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "존재하지 않는 게시물입니다."