from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    comment_id: str
    commenter_user_id: str
    commenter: str
    comment: str
    create_ts: datetime

