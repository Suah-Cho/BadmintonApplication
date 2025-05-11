from os import access

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import BaseResponse
from app.domains.auth.exceptions import TokenNotFound
from app.domains.auth.schemas import TokenDTO
from app.domains.auth.service import authenticate_user
from database.session import get_db

auth_router = APIRouter()

@auth_router.post("/login", response_model=BaseResponse[TokenDTO])
async def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
):
    """
    # 로그인
    ### Request Body
    - username: str
    - password: str

    ### Response
    - 200: BaseResponse
    - 401: 아이디 / 비밀번호 일치하지 않음
    - 404: 존재하지 않는 계정
    """

    token_data: TokenDTO = await authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    response.headers["Access-Control-Expose-Headers"] = "Set-Cookie"
    response.set_cookie(
        key="access_token",
        value=token_data.access_token,
        httponly=True,
        max_age=30 * 24 * 60 * 60,
    )

    return BaseResponse(data=token_data, message="로그인되었습니다.")

@auth_router.get("/logout", response_model=BaseResponse)
async def logout(
        request: Request,
        response: Response,
):
    """
    # 로그아웃
    ### Response
    - 200: BaseResponse
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise TokenNotFound()

    response.delete_cookie("access_token")

    return BaseResponse(message="로그아웃되었습니다.", data=None)