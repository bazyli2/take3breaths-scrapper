from typing import Annotated, List
from pydantic import BaseModel, Field
import requests
import os

from take3breaths_scrapper.settings import get_settings
from take3breaths_scrapper.types import AccessId, Description, FileName, Name

settings = get_settings()


class Track(BaseModel):
    name: Name
    image_url: Annotated[str, Field(validation_alias="image", exclude=True)]
    audio_file_url: Annotated[str, Field(validation_alias="signed_url", exclude=True)]
    sample_url: Annotated[str, Field(validation_alias="sample", exclude=True)]
    description: Description
    image_file_name: FileName = Field(validation_alias="image")
    audio_file_name: FileName = Field(validation_alias="signed_url")
    sample_file_name: FileName = Field(validation_alias="sample")
    access_id: AccessId = Field(validation_alias="access")
    tags: Annotated[List[str], Field(validation_alias="track_purposes", exclude=True)]

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


class Tag(BaseModel):
    name: Name


class TrackTagAssociation(BaseModel):
    track_name: str
    tag_name: str
