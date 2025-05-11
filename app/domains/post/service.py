from unicodedata import category

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostDTO


async def get_post_list(*, db: AsyncSession) -> list[PostDTO]:

    repo = PostRepository(db=db)
    rows = await repo.get_all_posts()

    posts = [PostDTO(
                post_id=post.post_id,
                title=post.title,
                content=post.content,
                category=post.category,
                writer_id=post.writer_id,
                writer=writer,
                writer_nickname=writer_nickname,
                create_ts=post.create_ts,
                update_ts=post.update_ts,)
            for post, writer, writer_nickname in rows]

    return posts