from functools import partial
from .use_case import use_case
from .db_describe_logic import describe
from .new_listing_preparations import prepare_new_listing_before_publish
from .parse_video_into_state_dict import parse_video_into_state_dict
from use_cases.db_operation_utils.concrete import (
    search_one_in_database,
    update_in_database
)

update_video_use_case = partial(
    use_case,
    search_one_in_database_fn=search_one_in_database,
    update_in_database_fn=update_in_database,
    describe_videos_in_database_fn=describe,
    prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
    parse_video_into_state_dict_fn=parse_video_into_state_dict
)
