from functools import partial
from .use_case import use_case
from .helpers import is_access_allowed

get_watch_video_record_use_case = partial(
    use_case,
    is_access_allowed_fn=is_access_allowed
)
