import csv
from pydantic import BaseModel


def save_objects_to_csv[T: BaseModel](objects: list[T], file_path: str):
    if not objects:
        raise ValueError("models not provided")
    schema = objects[0].model_json_schema(mode="serialization")
    fieldnames = list(schema["properties"].keys())
    with open(file_path, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for object in objects:
            writer.writerow(object.model_dump())
