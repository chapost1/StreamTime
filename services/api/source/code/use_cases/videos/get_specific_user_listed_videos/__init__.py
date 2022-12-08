from functools import partial
from .use_case import use_case
from entities.videos import NextPage, VideosPage
from .db_describe_logic import describe
from use_cases.db_operation_utils.concrete import search_in_database

get_specific_user_listed_videos_use_case = partial(
    use_case,
    search_in_database_fn=search_in_database,
    describe_videos_in_database_fn=describe,
    next_page_text_decoder=NextPage,
    next_videos_page_calculator=VideosPage
)
