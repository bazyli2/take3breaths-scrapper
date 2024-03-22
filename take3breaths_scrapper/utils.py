import csv
from pydantic import BaseModel

from take3breaths_scrapper.schema import Track


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


def save_insert_statements_to_file(objects: list[Track], file_path: str):
    with open(file_path, "w") as file:
        for obj in objects:
            file.write(generate_insert_statement(obj, "tracks") + "\n")


def generate_insert_statement(object: BaseModel, table_name: str):
    fieldnames = list(
        object.model_json_schema(mode="serialization")["properties"].keys()
    )
    fields = ", ".join(fieldnames)
    values = ", ".join(map(str, object.model_dump().values()))
    stmt = f"INSERT INTO {table_name} ({fields}) VALUES ({values});"
    return stmt
