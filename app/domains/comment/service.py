from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.comment.repository import CommentRepository
from app.domains.comment.schemas import CommentDTO


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
