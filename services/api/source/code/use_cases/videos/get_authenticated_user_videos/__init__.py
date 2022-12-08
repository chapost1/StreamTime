from functools import partial
from .use_case import use_case
from .db_describe_logic import (
    describe_unprocessed_videos,
    describe_videos
)
from use_cases.db_operation_utils.concrete import search_in_database

get_authenticated_user_videos_use_case = partial(
    use_case,
    search_in_database_fn=search_in_database,
    describe_unprocessed_videos_in_database_fn=describe_unprocessed_videos,
    describe_videos_in_database_fn=describe_videos,
)
