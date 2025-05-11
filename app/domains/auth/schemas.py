from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TokenDataDTO(BaseModel):
    sub: str
    id: str
    username: str
    nickname: str
    exp: Optional[datetime] = None

class TokenDTO(BaseModel):
    access_token: str
    sub: str
    id: str