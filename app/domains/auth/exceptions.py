from fastapi import status

from app.common.exception import CustomException

class PasswordNoMatch(CustomException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "비밀번호가 일치하지 않습니다."