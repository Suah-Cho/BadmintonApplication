from fastapi import APIRouter, Depends

from app.common.response import BaseResponse
from app.domains.auth.schemas import TokenDataDTO
from app.domains.auth.utils import authorize_user
from app.domains.files.schemas import PresignedURLDTO, S3FileDTO
from app.domains.files.service import generate_presigned_urls

file_router = APIRouter()

@file_router.post("", response_model=BaseResponse[list[S3FileDTO]])
async def presigned_url(
        files: list[PresignedURLDTO],
        user: TokenDataDTO = Depends(authorize_user),
):
    urls = await generate_presigned_urls(files=files)

    return BaseResponse(data=urls, message="Presigned URLs generated successfully.")