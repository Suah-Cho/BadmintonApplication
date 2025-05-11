import uuid

from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.sql import func

from app.models.base import Base

class Users(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(String(255), nullable=False)
    username = Column(String(30), nullable=False)
    nickname = Column(String(30), nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    profile_image_url = Column(Text, server_default=func.now())
    create_ts = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    delete_ts = Column(TIMESTAMP, nullable=True)