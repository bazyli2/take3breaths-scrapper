from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    images_directory: str = "images"
    audio_directory: str = "audio"


@lru_cache
def get_settings():
    return Settings()
