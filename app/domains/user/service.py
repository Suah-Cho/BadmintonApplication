
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.domains.user.models import Users


async def get_users_from_db(*, db: AsyncSession):
    result = await db.execute(
        select(Users)
    )
    return result.scalars().all()