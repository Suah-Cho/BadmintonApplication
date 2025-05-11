from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt
from app.core.config import config
from app.core.hash import verify_password
from app.domains.auth.exceptions import *
from app.domains.auth.schemas import *
from app.domains.user.exceptions import UserNotExists
from app.domains.user.repository import UserRepository
from app.repository.memory import BaseCacheRepository

async def authenticate_user(
        *, db: AsyncSession, username: str, password: str
) -> TokenDTO:
    repo = UserRepository(db=db)

    # 존재하는 사용자인지 확인
    user = await repo.get_user_by_id(id=username)
    if not user:
        raise UserNotExists()

    # 비밀번호 확인
    if not verify_password(password, user.password):
        raise PasswordNoMatch()

    # 토큰 발급
    token_data = TokenDataDTO(
        sub=user.user_id,
        id=user.id,
        username=user.username,
        nickname=user.nickname,
    )
    access_token = create_jwt_token(token_data, expires_delta=timedelta(minutes=30 * 24 * 30))

    return TokenDTO(access_token=access_token, sub=user.user_id, id=user.id)


def create_jwt_token(
        data: TokenDataDTO,
        expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.model_dump()

    if expires_delta:
        to_encode.update({"exp": datetime.now() + expires_delta})
    else:
        to_encode.update({"exp": datetime.now() + timedelta(minutes=15)})

    return jwt.encode(to_encode, config.SECRET, algorithm="HS256")
