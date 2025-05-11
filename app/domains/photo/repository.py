from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.domains.photo.models import Photo


class PhotoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, target_id: str):
        result = await self.db.execute(
            select(Photo).where(Photo.target_id == target_id)
        )
        return result.scalars().all()

    async def get_all_urls(self, target_id: str):
        result = await self.db.execute(
            select(Photo.url).where(Photo.target_id == target_id)
        )
        return result.scalars().all()

    async def create(self, photos: list[Photo]):
        for photo in photos:
            self.db.add(photo)
        return photos

    async def delete(self, target_id: str):
        result = await self.db.execute(
            select(Photo).where(Photo.target_id == target_id)
        )
        photos = result.scalars().all()
        for photo in photos:
            await self.db.delete(photo)
        return photos