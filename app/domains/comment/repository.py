from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.domains.comment.exceptions import CommentNotFound
from app.domains.comment.models import Comment
from app.domains.user.models import User


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, post_id: str):
        result = await self.db.execute(
            select(Comment, User.username.label("commenter_name"), User.nickname.label("commenter_nickname")).join(User, Comment.commenter_id == User.user_id).where(Comment.post_id == post_id)
        )
        return result.all()

    async def get_comment(self, comment_id: str):
        result = await self.db.execute(
            select(Comment).where(Comment.comment_id == comment_id)
        )
        return result.scalars().first()

    async def create(self, comment: Comment):
        self.db.add(comment)
        return comment

    async def update(self, comment: str, comment_id: str):
        existing_comment = await self.get_comment(comment_id=comment_id)
        if not existing_comment:
            raise CommentNotFound()

        existing_comment.comment = comment

        await self.db.commit()
        return comment