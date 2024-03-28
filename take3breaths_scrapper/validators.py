from typing import Literal


def replace_empty_with_none(v: str):
    return None if v == "" else v


def sql_serializer(v: str | None):
    return "NULL" if v is None else f"'{v}'"


def replace_single_quotes(v: str):
    return v.replace("'", "''")


def remove_new_lines(v: str):
    return v.replace("\n", "")


def get_last_url_segment(v: str):
    return v.split("/")[-1]


def remove_query_string(v: str):
    return v.split("?")[0]


def access_prefix_to_id(prefix: Literal["a", "r", "p"]):
    if prefix == "a":
        return "all"
    if prefix == "r":
        return "regular"
    if prefix == "p":
        return "premium"
