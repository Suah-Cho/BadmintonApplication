from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settigns(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str

    model_config = ConfigDict(env_file=".env")  # type: ignore

config = Settigns()  # type: ignore