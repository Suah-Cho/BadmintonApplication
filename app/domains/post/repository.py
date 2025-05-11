from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.domains.post.models import Post
from app.domains.user.models import User


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Post, User.username.label("writer"), User.nickname.label("writer_nickname"))
            .join(User, Post.writer_id == User.user_id)
        )
        return result.all()

    async def get(self, post_id: str):
        result = await self.db.execute(
            select(Post).where(Post.post_id == post_id)
        )
        return result.scalar_one_or_none()

    async def create(self, post: Post):
        self.db.add(post)
        return post

    async def delete(self, post_id: str):
        post = await self.get(post_id)
        if post:
            await self.db.delete(post)
            await self.db.commit()
            return True
        return False