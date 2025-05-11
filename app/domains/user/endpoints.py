from fastapi import APIRouter, Depends, Request

from app.common.response import BaseResponse
from app.domains.auth.exceptions import TokenNotFound
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
        request: Request,
        user_id: str,
        db: AsyncSession = Depends(get_db),
):
    """
    # 회원 프로필 조회
    ### Response
    - 200: BaseResponse
    - 401: 권한 없음
    - 404: 존재하지 않는 아이디
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise TokenNotFound()

    user = await get_user_profile(db=db, user_id=user_id)

    return BaseResponse(message="회원 프로필 조회를 성공했습니다.", data=user)

