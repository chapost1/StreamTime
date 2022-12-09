from functools import partial
from use_cases.videos.explore_listed_videos.helpers.get_visibility_settings import (
    get_visibility_settings as __get_visibility_settings
)
from use_cases.validation_utils.concrete import is_anonymous_user

get_visibility_settings = partial(
    __get_visibility_settings,
    is_anonymous_user_fn=is_anonymous_user
)
