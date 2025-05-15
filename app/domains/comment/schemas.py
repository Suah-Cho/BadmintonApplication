from datetime import datetime

from pydantic import BaseModel


class CommentDTO(BaseModel):
    comment_id: str
    commenter_user_id: str
    commenter_name: str
    commenter_nickname: str
    comment: str
    create_ts: datetime


class CreateCommentDTO(BaseModel):
    comment: str
    
    
class DefaultComment(BaseModel):
    comment_id: str

