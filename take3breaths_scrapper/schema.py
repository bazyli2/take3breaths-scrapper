from typing import Annotated, Any
from pydantic import AfterValidator, BaseModel, Field, computed_field
import requests
import os

from take3breaths_scrapper.settings import get_settings

settings = get_settings()


class Track(BaseModel):
    name: str
    image_url: Annotated[str, Field(validation_alias="image", exclude=True)]
    audio_file_url: Annotated[str, Field(validation_alias="signed_url", exclude=True)]
    sample_url: Annotated[str, Field(validation_alias="sample", exclude=True)]
    description: Annotated[str, AfterValidator(lambda v: v.replace("\n", "").strip())]
    access: str
    category: str

    @computed_field
    @property
    def image_file_name(self) -> str:
        return self.image_url.split("/")[-1]

    @computed_field
    @property
    def audio_file_name(self) -> str:
        url = self.audio_file_url.split("?")[0]
        return url.split("/")[-1]

    @computed_field
    @property
    def sample_file_name(self) -> str:
        return self.sample_url.split("/")[-1]

    def download_sample(self):
        response = requests.get(self.sample_url)
        os.makedirs(settings.samples_directory, exist_ok=True)
        with open(
            os.path.join(settings.samples_directory, self.sample_file_name), "wb"
        ) as file:
            file.write(response.content)

    def download_audio(self):
        response = requests.get(self.audio_file_url)
        os.makedirs(settings.audio_directory, exist_ok=True)
        with open(
            os.path.join(settings.audio_directory, self.audio_file_name), "wb"
        ) as file:
            file.write(response.content)

    def download_image(self):
        response = requests.get(self.image_url)
        os.makedirs(settings.images_directory, exist_ok=True)
        with open(
            os.path.join(settings.images_directory, self.image_file_name), "wb"
        ) as file:
            file.write(response.content)
