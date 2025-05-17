from datetime import date, time, datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, RootModel

class BaseWorkoutDTO(BaseModel):
    workout_id: str

class WorkoutDTO(BaseModel):
    workout_id: str
    user_id: str
    workout_date: date
    start: time
    end: time
    title: str
    content: Optional[str] = None
    color: str
    image_url: Optional[list[str]] = None
    create_ts: datetime

class CreateWorkoutDTO(BaseModel):
    date: date
    start: time
    end: time
    title: str
    content: Optional[str] = None
    color: str
    image_url: Optional[list[str]] = None

class WorkoutSummaryDTO(BaseModel):
    time: str
    title: str
    content: str
    color: str
    image_url: Optional[list[str]] = None

class GroupedWorkoutDTO(RootModel[Dict[str, List[WorkoutSummaryDTO]]]):
    pass