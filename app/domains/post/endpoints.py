from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import BaseResponse
from app.domains.post.schemas import PostDTO
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