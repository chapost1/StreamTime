from functools import partial
from .use_case import use_case
from entities.videos import NextPage, VideosPage
from .describe_logic import describe
from .visibility_settings import get_visibility_settings as __get_visibility_settings
from use_cases.validation_utils import is_anonymous_user

get_visibility_settings = partial(__get_visibility_settings, is_anonymous_user_fn=is_anonymous_user)

explore_listed_videos_use_case = partial(
    use_case,
    describe_videos_fn=describe,
    get_visibility_settings_fn=get_visibility_settings,
    next_page_text_decoder=NextPage,
    next_videos_page_calculator=VideosPage
)
