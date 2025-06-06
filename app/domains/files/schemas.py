import enum

from pydantic import BaseModel


class TypeEnum(enum.Enum):
    workout = "workout"
    post = "post"

class PresignedURLDTO(BaseModel):
    file_name: str
    content_type: str

class S3FileDTO(BaseModel):
    file_name: str
    content_type: str
    url: str