from functools import partial
from .use_case import use_case
from .describe_logic import describe
from .new_listing_preparations import prepare_new_listing_before_publish
from .parse_video_into_state_dict import parse_video_into_state_dict
from use_cases.db_operation_utils.concrete import (
    search_db,
    update_db
)

update_video_use_case = partial(
    use_case,
    search_db_fn=search_db,
    update_db_fn=update_db,
    describe_videos_fn=describe,
    prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
    parse_video_into_state_dict_fn=parse_video_into_state_dict
)
