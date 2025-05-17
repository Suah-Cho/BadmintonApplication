import uuid

from sqlalchemy import Column, String, Date, Time, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Workout(Base):
    __tablename__ = "workouts"

    workout_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    workout_date = Column(Date, nullable=False)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    color = Column(Text, nullable=False)
    create_ts = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_ts = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    delete_ts = Column(TIMESTAMP, nullable=True)

    photos = relationship(
        "Photo",
        back_populates="workout",
        primaryjoin="Workout.workout_id == foreign(Photo.target_id)",
        cascade="all, delete-orphan"
    )