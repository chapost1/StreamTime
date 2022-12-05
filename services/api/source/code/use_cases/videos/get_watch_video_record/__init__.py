from functools import partial
from .use_case import use_case
from .describe_logic import describe
from use_cases.validation_utils.concrete import is_same_user
from use_cases.db_operation_utils.concrete import search_db
from .is_access_allowed import is_access_allowed as __is_access_allowed

is_access_allowed = partial(__is_access_allowed, is_same_user_fn=is_same_user)

get_watch_video_record_use_case = partial(
    use_case,
    search_db_fn=search_db,
    describe_videos_fn=describe,
    is_access_allowed_fn=is_access_allowed
)
