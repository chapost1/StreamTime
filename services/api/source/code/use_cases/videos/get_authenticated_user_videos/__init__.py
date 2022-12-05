from functools import partial
from .use_case import use_case
from .describe_logic import (
    describe_unprocessed_videos,
    describe_videos
)
from use_cases.db_operation_utils.concrete import search_db

get_authenticated_user_videos_use_case = partial(
    use_case,
    search_db_fn=search_db,
    describe_unprocessed_videos_fn=describe_unprocessed_videos,
    describe_videos_fn=describe_videos,
)
