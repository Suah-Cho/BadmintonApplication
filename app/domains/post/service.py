import logging
import uuid
from datetime import datetime
from unicodedata import category

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.photo.repository import PhotoRepository
from app.domains.post.models import Post
from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostDTO, CreatePostDTO
from app.domains.photo.service import save_photo_list


async def get_post_list(*, db: AsyncSession) -> list[PostDTO]:

    post_repo = PostRepository(db=db)
    rows = await post_repo.get_all()

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

async def create_post(*, db: AsyncSession, post: CreatePostDTO, user_id: str) -> str:
    post_repo = PostRepository(db=db)

    print(post.image_url)
    new_post = Post(
        post_id=str(uuid.uuid4()),
        title=post.title,
        content=post.content,
        category=post.category,
        writer_id=user_id,
        create_ts=datetime.now(),
    )

    try:
        async with db.begin():
            await save_photo_list(urls=post.image_url, target_id=new_post.post_id, type="post", db=db)
            await post_repo.create(new_post)
        return new_post.post_id
    except Exception as e:
        logging.error(e)
        raise DBException()