import enum

from pydantic import BaseModel


class TypeEnum(enum.Enum):
    workout = "workout"
    post = "post"