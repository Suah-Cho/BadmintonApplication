import enum
import uuid

from sqlalchemy import Column, String, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func

from app.domains.post.schemas import PostCategoryEnum
from app.models.base import Base

class Comment(Base):
    __tablename__ = "post_comments"

    comment_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String(36), nullable=False)
    commenter_id = Column(String(36), nullable=False)
    comment = Column(Text, nullable=False)
    create_ts = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    delete_ts = Column(TIMESTAMP, nullable=True)