import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.domains.comment.schemas import CommentDTO


class PostCategoryEnum(enum.Enum):
    notice = "notice"
    court = "court"
    equipment = "equipment"
    etc = "etc"

class PostDTO(BaseModel):
    post_id: str
    writer_id: str
    writer: str
    writer_nickname: str
    title: str
    content: str
    category: PostCategoryEnum
    create_ts: datetime
    update_ts: Optional[datetime] = None

    class Config:
        from_attributes = True

class CreatePostDTO(BaseModel):
    title: str
    content: str
    category: PostCategoryEnum
    image_url: list[str]

class DefaultPost(BaseModel):
    post_id: str

class PostDetailDTO(BaseModel):
    post_id: str
    writer_id: str
    writer: str
    writer_nickname: str
    title: str
    content: str
    category: PostCategoryEnum
    image_urls: Optional[list[str]] = None
    comments: Optional[list[CommentDTO]] = None
    create_ts: datetime
    update_ts: Optional[datetime] = None