from pydantic import BaseModel, Field, computed_field
import requests
import os

from take3breaths_scrapper.settings import get_settings

settings = get_settings()


class Track(BaseModel):
    name: str
    image_url: str = Field(validation_alias="image")

    @computed_field
    @property
    def image_file_name(self) -> str:
        return self.image_url.split("/")[-1]

    def download_image(self):
        response = requests.get(self.image_url)
        os.makedirs(settings.images_directory, exist_ok=True)
        with open(
            os.path.join(settings.images_directory, self.image_file_name), "wb"
        ) as file:
            file.write(response.content)
