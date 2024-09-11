import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = ".env"

    api_key: str = os.getenv("API_KEY")
    base_url: str = os.getenv("BASE_URL")
    model: str = os.getenv("MODEL")


settings = Config()
