from typing import Annotated, Literal

from pydantic import AfterValidator

from take3breaths_scrapper.validators import (
    access_prefix_to_id,
    get_last_url_segment,
    remove_new_lines,
    remove_query_string,
    replace_single_quotes,
    wrap_in_quotes,
)


Name = Annotated[
    str,
    AfterValidator(wrap_in_quotes),
]

Description = Annotated[
    str,
    AfterValidator(remove_new_lines),
    AfterValidator(replace_single_quotes),
    AfterValidator(wrap_in_quotes),
]
AccessPrefix = Literal["a", "r", "p"]


AccessId = Annotated[
    str, AfterValidator(access_prefix_to_id), AfterValidator(wrap_in_quotes)
]

FileName = Annotated[
    str,
    AfterValidator(remove_query_string),
    AfterValidator(get_last_url_segment),
    AfterValidator(wrap_in_quotes),
]
