from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settigns(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET: str

    model_config = ConfigDict(env_file=".env")  # type: ignore

config = Settigns()  # type: ignore