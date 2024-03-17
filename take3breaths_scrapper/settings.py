from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    images_directory: str = "assets/images"
    audio_directory: str = "assets/audio"
    samples_directory: str = "assets/samples"


@lru_cache
def get_settings():
    return Settings()
