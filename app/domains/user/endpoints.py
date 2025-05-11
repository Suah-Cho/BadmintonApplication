from fastapi import APIRouter, Depends, Request

from app.common.response import BaseResponse
from app.domains.auth.exceptions import TokenNotFound, NotAuthorization
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.user.schemas import CreateUserDTO, UserDTO
from app.domains.user.service import *
from database.session import get_db

user_router = APIRouter()

@user_router.post("", response_model=BaseResponse[UserDTO])
async def post_users(
        create_user_dto: CreateUserDTO,
        db: AsyncSession = Depends(get_db),
):
    """
    # 회원 가입
    ### Request Body
    - id: str
    - username: str
    - email: str
    - phone: str
    - password: str
    - profile_image_url: str

    ## Response
    - 200: BaseResponse
    - 409: 존재하는 아이디 or 등록된 이메일/전화번호
    """

    new_user = await create_user(db=db, user_dto=create_user_dto)

    return BaseResponse(message="회원 가입을 성공했습니다.", data=new_user)

@user_router.delete("/{user_id}", response_model=BaseResponse[None])
async def delete_user(
        user_id: str,
        db: AsyncSession = Depends(get_db),
):
    """
    # 회원 탈퇴
    ### Response
    - 200: BaseResponse
    - 401: 권한 없음
    - 404: 존재하지 않는 아이디
    """
    await delete_user(db=db, user_id=user_id)

    return BaseResponse(message="회원 탈퇴를 성공했습니다.", data=None)

@user_router.get("/{user_id}/profile", response_model=BaseResponse[UserDTO])
async def get_profile(
        user_id: str,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 회원 프로필 조회
    ### Response
    - 200: BaseResponse
    - 401: 권한 없음
    - 404: 존재하지 않는 아이디
    """
    if user.sub != user_id:
        raise NotAuthorization()

    user = await get_user_profile(db=db, user_id=user.sub)

    return BaseResponse(message="회원 프로필 조회를 성공했습니다.", data=user)

@user_router.put("/{user_id}/password", response_model=BaseResponse[None])
async def put_password(
        user_id: str,
        password_dto: PasswordDTO,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 비밀번호 변경
    ### Response
    - 200: BaseResponse
    - 400: 현재 비밀번호 오류
    - 401: 로그인 필요
    - 403: 권한 없음
    - 422: 새로운 비밀번호 불가
    """
    if user.sub != user_id:
        raise NotAuthorization()

    await update_user_password(db=db, user_id=user.sub, password_dto=password_dto)

    return BaseResponse(message="비밀번호 변경을 성공했습니다.", data=None)

@user_router.put("/{user_id}/profile", response_model=BaseResponse[UserDTO])
async def put_profile(
        user_id: str,
        profile_dto: ProfileDTO,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 프로필 수정
    ### Request Body
    - profile_image_url: str
    - nickname: str
    ### Response
    - 200: BaseResponse
    - 401: 로그인 필요
    - 403: 권한 없음
    """
    if user.sub != user_id:
        raise NotAuthorization()

    result = await update_profile(db=db, user_id=user.sub, profile_dto=profile_dto)

    return BaseResponse(message="프로필 수정을 성공했습니다.", data=result)