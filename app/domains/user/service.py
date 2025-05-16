import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.auth.exceptions import PasswordNoMatch
from app.domains.post.repository import PostRepository
from app.domains.post.schemas import PostDTO
from app.domains.user.exceptions import *
from app.domains.user.models import User
from app.domains.user.repository import UserRepository
from app.core.hash import password_hash, verify_password
from app.domains.user.schemas import *


async def create_user(
        *, db: AsyncSession, user_dto: CreateUserDTO
):
    repo = UserRepository(db=db)

    # 아이디 중복 체크
    existing_user = await repo.get_user_by_id(user_dto.id)
    if existing_user:
        raise IDAlreadyExists()
    # 이메일 중복 체크
    existing_email = await repo.get_user_by_email(user_dto.email)
    if existing_email:
        raise EmailAlreadyExists()

    hash_password = password_hash(user_dto.password)

    new_user = User(
        user_id=str(uuid.uuid4()),
        id=user_dto.id,
        username=user_dto.username,
        nickname=user_dto.nickname,
        password=hash_password,
        email=user_dto.email,
        phone=user_dto.phone,
        profile_image_url=user_dto.profile_image_url,
        create_ts=datetime.now(),
    )
    try:
        return await repo.create(new_user)
    except Exception as e:
        raise NicknameAlreadyExists()

async def delete_user(
        *, db: AsyncSession, user_id: str
):
    repo = UserRepository(db=db)
    if not await repo.delete(user_id):
        raise UserNotExists()

async def get_user_profile(
        *, db: AsyncSession, user_id: str
) -> UserDTO:
    repo = UserRepository(db=db)

    user = await repo.get_user(user_id=user_id)
    if not user:
        raise UserNotExists()

    return user

async def update_user_password(*, db: AsyncSession, user_id: str, password_dto: PasswordDTO):
    repo = UserRepository(db=db)

    user = await repo.get_user(user_id=user_id)
    if not user:
        raise UserNotExists()

    # 비밀번호 확인
    if not verify_password(password_dto.password, user.password):
        raise PasswordNoMatch()

    # 비밀번호 변경 확인
    hash_password = password_hash(password_dto.new_password)
    if user.password == hash_password:
        raise SamePassword()

    user.password = hash_password

    try:
        return await repo.update(user=user)
    except Exception as e:
        raise DBException()

async def update_profile(*, db: AsyncSession, user_id: str, profile_dto: ProfileDTO):
    repo = UserRepository(db=db)

    user = await repo.get_user(user_id=user_id)

    if not user:
        raise UserNotExists()

    user.nickname = profile_dto.nickname
    user.profile_image_url = profile_dto.profile_image_url

    try:
        return await repo.update(user=user)
    except Exception as e:
        raise DBException()

async def get_posts_for_user(
        *, db: AsyncSession, user_id: str
) -> list[PostDTO] :
    repo = PostRepository(db=db)
    rows = await repo.get_by_writer_id(writer_id=user_id)

    posts = [PostDTO(
        post_id=post.post_id,
        title=post.title,
        content=post.content,
        category=post.category,
        writer_id=post.writer_id,
        writer=writer,
        writer_nickname=writer_nickname,
        create_ts=post.create_ts,
        update_ts=post.update_ts, )
        for post, writer, writer_nickname in rows]

    return posts