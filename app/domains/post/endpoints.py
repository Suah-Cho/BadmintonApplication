from fastapi import APIRouter, Depends
from psycopg.errors import CrashShutdown
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import BaseResponse
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.post.schemas import PostDTO, CreatePostDTO, DefaultPost
from app.domains.post.service import *
from database.session import get_db

post_router = APIRouter()

@post_router.get("", response_model=BaseResponse[list[PostDTO]])
async def get_posts(
        db: AsyncSession = Depends(get_db),
):
    """
    # 게시판 조회
    ### Response
    - 200: BaseResponse
    """

    result = await get_post_list(db=db)

    return BaseResponse(message="게시판을 조회했습니다.", data=result)

@post_router.post("", response_model=BaseResponse[DefaultPost], status_code=201)
async def post_post(
        post: CreatePostDTO,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 게시물 등록
    ### Request Body
    - title: str
    - content: str
    - category: str
    - image_url: list[str]
    ### Response
    - 201: BaseResponse
    - 400: 잘못된 요청
    - 401: 권한 없음
    """
    post_id = await create_post(db=db, post=post, user_id=user.sub)

    return BaseResponse(message="게시물을 등록했습니다.", data={
        "post_id": post_id
    })

@post_router.put("/{post_id}", response_model=BaseResponse[DefaultPost])
async def put_post(
        post_id: str,
        post: CreatePostDTO,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 게시물 수정
    ### Request Body
    - title: str
    - content: str
    - category: str
    - image_url: list[str]
    ### Response
    - 200: BaseResponse
    - 403: 권한 없음
    """
    await check_post_authorization(db=db, post_id=post_id, user=user)

    post_id = await update_post(db=db, post_id=post_id, put_post=post)

    return BaseResponse(message="게시물을 수정했습니다.", data={
        "post_id": post_id
    })

@post_router.delete("/{post_id}", status_code=204)
async def delete_post_id(
        post_id: str,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 게시물 삭제
    ### Response
    - 204: BaseResponse
    - 403: 권한 없음
    """
    await check_post_authorization(db=db, post_id=post_id, user=user)

    await delete_post(db=db, post_id=post_id)

    return None


