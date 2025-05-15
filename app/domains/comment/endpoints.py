from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.response import BaseResponse
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.comment.schemas import CreateCommentDTO, DefaultComment
from app.domains.comment.service import *
from database.session import get_db

comment_router = APIRouter(tags=["Comment"])


@comment_router.post("", 
               response_model=BaseResponse[DefaultComment], 
               status_code=status.HTTP_201_CREATED)
async def post_comment(
    post_id: str,
    comment: CreateCommentDTO,
    db: AsyncSession = Depends(get_db),
    user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 댓글 작성
    ### Request Body
    - comment: str
    ### Response
    - 201: BaseResponse
    - 400: 잘못된 요청
    - 401: 권한 없음
    """
    comment_id = await create_comment(db=db, post_id=post_id, comment=comment, user_id=user.sub)
    
    return BaseResponse(message="댓글이 작성되었습니다.", data={
        "comment_id": comment_id
    })

@comment_router.put("/{comment_id}", response_model=BaseResponse[DefaultComment])
async def put_comment(
        comment_id: str,
        comment: CreateCommentDTO,
        db: AsyncSession = Depends(get_db),
        user: TokenDataDTO = Depends(authorize_user),
):
    """
    # 댓글 수정
    ### Request Body
    - comment: str
    ### Response
    - 200: BaseResponse
    - 403: 권한 없음
    """

    await check_comment_authorization(db=db, user_id=user.sub, comment_id=comment_id)

    comment_id = await update_comment(db=db, comment_id=comment_id, comment=comment)

    return BaseResponse(message="댓글이 수정되었습니다.", data={
        "comment_id": comment_id
    })