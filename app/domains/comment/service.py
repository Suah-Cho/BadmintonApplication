import logging
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.comment.models import Comment
from app.domains.comment.repository import CommentRepository
from app.domains.comment.schemas import CommentDTO, CreateCommentDTO


async def get_comments(*, db: AsyncSession, post_id: str) -> list[CommentDTO]:
    comment_repo = CommentRepository(db=db)

    rows = await comment_repo.get_all(post_id=post_id)

    comments = [CommentDTO(
        comment_id=comment.comment_id,
        commenter_user_id=comment.comment_id,
        commenter_name=commenter_name,
        commenter_nickname=commenter_nickname,
        comment=comment.comment,
        create_ts=comment.create_ts,
    ) for comment, commenter_name, commenter_nickname in rows]

    return comments


async def create_comment(*, db: AsyncSession, post_id: str, comment: CreateCommentDTO, user_id: str) -> str:
    comment_repo = CommentRepository(db=db)
    
    new_comment = Comment(
        comment_id=str(uuid.uuid4()),
        post_id=post_id,
        commenter_id=user_id,
        comment=comment.comment,
        create_ts=datetime.now(),
    )
    
    try:
        async with db.begin():
            await comment_repo.create(new_comment)
        await db.commit()
        return new_comment.comment_id
    except Exception as e:
        logging.error(e)
        raise DBException()
