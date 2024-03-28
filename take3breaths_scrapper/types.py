from typing import Annotated

from pydantic import AfterValidator, PlainSerializer

from take3breaths_scrapper.validators import (
    access_prefix_to_id,
    get_last_url_segment,
    remove_new_lines,
    remove_query_string,
    replace_empty_with_none,
    replace_single_quotes,
    sql_serializer,
)

SQLString = Annotated[str, PlainSerializer(sql_serializer)]

Name = Annotated[
    SQLString,
    AfterValidator(replace_empty_with_none),
]

Description = Annotated[
    SQLString,
    AfterValidator(remove_new_lines),
    AfterValidator(replace_single_quotes),
    AfterValidator(replace_empty_with_none),
]


AccessId = Annotated[
    SQLString,
    AfterValidator(access_prefix_to_id),
]

FileName = Annotated[
    SQLString,
    AfterValidator(remove_query_string),
    AfterValidator(get_last_url_segment),
]
