from fastapi import status

from app.common.exception import CustomException

class PasswordNoMatch(CustomException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "비밀번호가 일치하지 않습니다."

class TokenNotFound(CustomException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "토큰이 유효하지 않습니다. 로그인을 진행해주세요."

class NotAuthorization(CustomException):
    status_code: int = status.HTTP_403_FORBIDDEN
    message: str = "권한이 없습니다."