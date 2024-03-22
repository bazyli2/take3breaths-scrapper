from typing import Annotated, Any
from pydantic import AfterValidator, BaseModel, Field, computed_field
import requests
import os

from take3breaths_scrapper.settings import get_settings

settings = get_settings()


def description_validator(description: str):
    value = description.replace("\n", "").strip().replace("'", "''")
    return "NULL" if value == "" else f"'{value}'"


class Track(BaseModel):
    name: Annotated[str, AfterValidator(lambda v: f"'{v}'")]
    image_url: Annotated[str, Field(validation_alias="image", exclude=True)]
    audio_file_url: Annotated[str, Field(validation_alias="signed_url", exclude=True)]
    sample_url: Annotated[str, Field(validation_alias="sample", exclude=True)]
    description: Annotated[str, AfterValidator(description_validator)]
    access: Annotated[str, Field(exclude=True)]
    category: Annotated[str, Field(exclude=True)]

    @computed_field
    @property
    def image_file_name(self) -> str:
        value = self.image_url.split("/")[-1]
        return f"'{value}'"

    @computed_field
    @property
    def audio_file_name(self) -> str:
        url = self.audio_file_url.split("?")[0]
        value = url.split("/")[-1]
        return f"'{value}'"

    @computed_field
    @property
    def sample_file_name(self) -> str:
        value = self.sample_url.split("/")[-1]
        return f"'{value}'"

    @computed_field
    @property
    def access_id(self) -> str:
        if self.access == "p":
            return "'premium'"
        if self.access == "a":
            return "'all'"
        if self.access == "r":
            return "'regular'"
        return "'all'"

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

    def generate_insert_statement(self, table_name: str):
        fieldnames = list(
            self.model_json_schema(mode="serialization")["properties"].keys()
        )
        fields = ", ".join(fieldnames)
        values = ", ".join(map(str, self.model_dump().values()))
        stmt = f"INSERT INTO {table_name} ({fields}) VALUES ({values});"
        return stmt
