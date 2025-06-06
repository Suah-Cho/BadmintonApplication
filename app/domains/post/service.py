import logging
import uuid
from datetime import datetime
from typing import Tuple, Union, Literal

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.auth.exceptions import NotAuthorization
from app.domains.auth.schemas import TokenDataDTO
from app.domains.comment.schemas import CommentDTO
from app.domains.comment.service import get_comments
from app.domains.post.exceptions import PostNotFound
from app.domains.post.models import Post
from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostDTO, CreatePostDTO, PostCategoryEnum
from app.domains.files.service import save_photo_list, change_photo_list, get_photo_list, delete_photo_lists


async def get_post_list(*, db: AsyncSession, category: Union[PostCategoryEnum, Literal["all"]]) -> list[PostDTO]:

    post_repo = PostRepository(db=db)
    if category == 'all':
        rows = await post_repo.get_all()
    else:
        rows = await post_repo.get_all_for_category(category=category)

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

async def update_post(*, db: AsyncSession, post_id: str, put_post: CreatePostDTO) -> str:
    post_repo = PostRepository(db=db)

    rows= await post_repo.get(post_id=post_id)
    if not rows:
        raise PostNotFound()
    
    post, _, _ = rows

    post.title = put_post.title
    post.content = put_post.content
    post.category = put_post.category
    post.update_ts = datetime.now()

    try:
        await change_photo_list(db=db, urls=put_post.image_url, target_id=post_id, type="post")
        await db.commit()
        return post_id
    except Exception as e:
        logging.error(e)
        raise DBException()

async def check_post_authorization(*, db: AsyncSession, post_id: str, user: TokenDataDTO) -> None:
    post_repo = PostRepository(db=db)
    try:
        post, writer, writer_nickname = await post_repo.get(post_id=post_id)
    except Exception:
        raise PostNotFound()

    if post.writer_id != user.sub:
        raise NotAuthorization()

async def delete_post(*, db: AsyncSession, post_id: str) -> None:
    post_repo = PostRepository(db=db)

    try:
        await post_repo.delete(post_id=post_id)
        await delete_photo_lists(db=db, target_id=post_id)
    except Exception as e:
        logging.error(e)
        raise DBException()

async def delete_post_for_user_id(*, db: AsyncSession, user_id: str) -> None:
    post_repo = PostRepository(db=db)

    posts = await post_repo.get_by_writer_id(writer_id=user_id)

    for post in posts:
        logging.error(f"======{post}")
        await delete_post(db=db, post_id=post.post_id)

async def get_post_by_post_id(*, db: AsyncSession, post_id: str)-> Tuple[PostDTO, list[CommentDTO], list[str]]:
    post_repo = PostRepository(db=db)

    result = await post_repo.get(post_id=post_id)

    if result is None:
        raise PostNotFound()
    post, writer, writer_nickname = result

    if not post:
        raise PostNotFound()

    post = PostDTO(
        post_id=post.post_id,
        title=post.title,
        content=post.content,
        category=post.category,
        writer_id=post.writer_id,
        writer=writer,
        writer_nickname=writer_nickname,
        create_ts=post.create_ts,
        update_ts=post.update_ts,
    )

    comments = await get_comments(db=db, post_id=post.post_id)
    urls = await get_photo_list(db=db, target_id=post.post_id)

    return post, comments, urls