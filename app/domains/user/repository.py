from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.domains.user.models import Users

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self):
        result = await self.db.execute(
            select(Users)
        )
        return result.scalars().all()

    async def get_user(self, user_id: str):
        result = await self.db.execute(
            select(Users).where(Users.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: str):
        result = await self.db.execute(
            select(Users).where(Users.id == id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(
            select(Users).where(Users.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user: Users):
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: str):
        user = await self.get_user_by_user_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False