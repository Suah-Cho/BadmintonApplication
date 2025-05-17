from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.exceptions import PostNotFound
from app.domains.post.repository import PostRepository


async def check_post(*, db: AsyncSession, post_id: str) -> None:
    post_repo = PostRepository(db=db)

    post = await post_repo.get(post_id=post_id)

    if not post:
        raise PostNotFound()