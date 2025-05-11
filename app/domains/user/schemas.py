from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserDTO(BaseModel):
    user_id: str
    id: str
    username: str
    nickname: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None
    create_ts: datetime

class CreateUserDTO(BaseModel):
    id: str
    username: str
    nickname: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    profile_image_url: Optional[str] = None