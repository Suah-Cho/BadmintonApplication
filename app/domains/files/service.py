import logging
import uuid
from datetime import datetime

import boto3
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception import DBException
from app.core.config import config
from app.domains.files.exceptions import PresignedURLException
from app.domains.files.models import Photo
from app.domains.files.repository import PhotoRepository
from app.domains.files.schemas import PresignedURLDTO, S3FileDTO


async def get_photo_list(*, db: AsyncSession, target_id: str) -> list[str]:
    photo_repo = PhotoRepository(db=db)

    files = await photo_repo.get_all_urls(target_id=target_id)

    presigned_urls = []
    s3_client = boto3.client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        endpoint_url="https://s3.ap-northeast-2.amazonaws.com"  # 🔥 추가!
    )
    try:
        for file in files:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': config.AWS_S3_BUCKET,
                    'Key': file
                },
                ExpiresIn=3600  # URL 유효 기간 (초 단위)
            )
            presigned_urls.append(presigned_url)
    except Exception as e:
        logging.error(e)
        raise PresignedURLException()

    return presigned_urls

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

async def generate_presigned_urls(*, files: list[PresignedURLDTO]) -> list[S3FileDTO]:
    s3_client = boto3.client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        endpoint_url="https://s3.ap-northeast-2.amazonaws.com"  # 🔥 추가!
    )

    try:
        presigned_urls = []
        for file in files:
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': config.AWS_S3_BUCKET,
                    'Key': file.file_name,
                    'ContentType': file.content_type or 'application/octet-stream'
                },
                ExpiresIn=3600  # URL 유효 기간 (초 단위)
            )
            presigned_urls.append(S3FileDTO(
                file_name=file.file_name,
                content_type=file.content_type,
                url=presigned_url
            ))

    except Exception as e:
        raise PresignedURLException()

    print("Generated presigned URLs:", presigned_urls)
    return presigned_urls