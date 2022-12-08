from functools import partial
from .use_case import use_case
from entities.videos import NextPage, VideosPage
from .db_describe_logic import describe
from .get_visibility_settings import get_visibility_settings as __get_visibility_settings
from use_cases.validation_utils.concrete import is_anonymous_user
from use_cases.db_operation_utils.concrete import search_in_database

get_visibility_settings = partial(__get_visibility_settings, is_anonymous_user_fn=is_anonymous_user)

explore_listed_videos_use_case = partial(
    use_case,
    search_in_database_fn=search_in_database,
    describe_videos_in_database_fn=describe,
    get_visibility_settings_fn=get_visibility_settings,
    next_page_text_decoder=NextPage,
    next_videos_page_calculator=VideosPage
)
