import logging

from fastapi import status

from app.common.exception import CustomException


class IDAlreadyExists(CustomException):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "사용중인 아이디입니다."

class EmailAlreadyExists(CustomException):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "사용중인 이메일입니다."

class PhoneAlreadyExists(CustomException):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "사용중인 전화번호입니다."

class UserNotExists(CustomException):
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "사용자를 찾을 수 없습니다."

class NicknameAlreadyExists(CustomException):
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "사용중인 닉네임입니다."

class SamePassword(CustomException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    message: str = "현재 비밀번호와 새 비밀번호가 동일합니다. 다른 비밀번호를 입력해주세요."