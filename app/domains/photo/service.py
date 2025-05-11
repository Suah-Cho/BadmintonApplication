import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.domains.photo.models import Photo
from app.domains.photo.repository import PhotoRepository

async def get_photo_list(*, db: AsyncSession, target_id: str) -> list[str]:
    photo_repo = PhotoRepository(db=db)

    urls = await photo_repo.get_all_urls(target_id=target_id)

    return urls

async def save_photo_list(*, db: AsyncSession, urls: list[str], target_id: str, type: str):

    photo_repo = PhotoRepository(db=db)

    photos = [
        Photo(
            photo_id=str(uuid.uuid4()),
            type=type,
            target_id=target_id,
            url=url,
            create_ts=datetime.now()
        )
        for url in urls
    ]

    try:
        await photo_repo.create(photos)
    except Exception as e:
        raise DBException()

async def change_photo_list(*, db: AsyncSession, urls: list[str], target_id: str, type: str):
    photo_repo = PhotoRepository(db=db)

    try:
        await photo_repo.delete(target_id=target_id)
        await save_photo_list(db=db, urls=urls, target_id=target_id, type=type)
    except Exception as e:
        raise DBException()

async def delete_photo_lists(*, db: AsyncSession, target_id: str):
    photo_repo = PhotoRepository(db=db)

    try:
        await photo_repo.delete(target_id=target_id)
    except Exception as e:
        raise DBException()