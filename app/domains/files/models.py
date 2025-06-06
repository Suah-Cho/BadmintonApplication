import enum
import uuid

from sqlalchemy import Column, String, Text, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.domains.files.schemas import TypeEnum
from app.models.base import Base

class Photo(Base):
    __tablename__ = "photos"

    photo_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(TypeEnum), nullable=False)
    target_id = Column(String(36), nullable=False)
    url = Column(Text, nullable=False)
    create_ts = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    delete_ts = Column(TIMESTAMP, nullable=True)

    workout = relationship(
        "Workout",
        back_populates="photos",
        primaryjoin="remote(Workout.workout_id) == foreign(Photo.target_id)"
    )