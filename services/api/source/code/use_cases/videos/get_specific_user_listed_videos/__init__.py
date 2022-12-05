from functools import partial
from .use_case import use_case
from entities.videos import NextPage, VideosPage
from .db_describe_logic import describe
from use_cases.db_operation_utils.concrete import search_db

get_specific_user_listed_videos_use_case = partial(
    use_case,
    search_db_fn=search_db,
    describe_db_videos_fn=describe,
    next_page_text_decoder=NextPage,
    next_videos_page_calculator=VideosPage
)
