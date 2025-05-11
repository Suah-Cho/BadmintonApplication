import enum
import uuid

from sqlalchemy import Column, String, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func

from app.domains.post.schemas import PostCategoryEnum
from app.models.base import Base

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    writer_id = Column(String(36), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(Enum(PostCategoryEnum), nullable=False)
    create_ts = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    delete_ts = Column(TIMESTAMP, nullable=True)