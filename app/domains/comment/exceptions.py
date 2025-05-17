from fastapi import status

from app.common.exception import CustomException


class CommentNotFound(CustomException):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "존재하지 않는 댓글입니다."