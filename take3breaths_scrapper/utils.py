from typing import Sequence
from pydantic import BaseModel


def save_insert_statements_to_file(
    objects: Sequence[BaseModel], table_name: str, file_path: str
):
    with open(file_path, "w") as file:
        for obj in objects:
            file.write(generate_insert_statement(obj, table_name) + "\n")


def generate_insert_statement(object: BaseModel, table_name: str):
    fieldnames = list(
        object.model_json_schema(mode="serialization")["properties"].keys()
    )
    fields = ", ".join(fieldnames)
    values = ", ".join(map(str, object.model_dump().values()))
    stmt = f"INSERT INTO {table_name} ({fields}) VALUES ({values});"
    return stmt
