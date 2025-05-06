import contextvars
from functools import wraps
import logging
from urllib.parse import quote
from typing import Awaitable, Callable, Generic, TypeVar, AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)

from app.core.config import config

DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_USER = config.DB_USER
DB_PASSWORD = quote(config.DB_PASSWORD)
DB_NAME = config.DB_NAME

session_context = contextvars.ContextVar("session_context")
engine = None
Session = None


def init_db():
    """
    데이터베이스 엔진 및 세션 팩토리 초기화
    :return:
    """
    global engine, Session

    DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_async_engine(
        DB_URL, echo=True, future=True
    )  # engine은 데이터베이스 연결을 관리
    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    Session = async_scoped_session(
        session_factory, scopefunc=lambda: session_context.get()
    )  # 세션은 데이터베이스와의 통신을 담당
    logging.info("Database engine and session initialized")


async def dispose_db():
    """
    애플리케이션 종료 시 데이터베이스 엔진 정리
    :return:
    """
    if engine:
        await engine.dispose()
        logging.info("Database engine disposed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    요청마다 세션 생성 및 반환
    :return:
    """

    if Session is None:
        raise RuntimeError("Session is not initialized")

    token = session_context.set(str(uuid4()))
    async with Session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            session_context.reset(token)


T = TypeVar("T")


class Transactional(Generic[T]):
    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def _transactional(*args, **kwargs) -> T:
            if Session is None:
                raise RuntimeError("Session is not initialized")

            session = Session()
            try:
                result: T = await func(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _transactional
