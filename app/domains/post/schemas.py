import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

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