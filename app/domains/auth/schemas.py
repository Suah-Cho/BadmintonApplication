from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TokenDataDTO(BaseModel):
    user_id: str
    id: str
    username: str
    nickname: str

class TokenDTO(BaseModel):
    access_token: str
    user_id: str
    id: str