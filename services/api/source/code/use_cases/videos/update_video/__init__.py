from functools import partial
from .use_case import use_case
from .describe_logic import describe
from .new_listing_preparations import prepare_new_listing_before_publish
from .parse_video_into_state_dict import parse_video_into_state_dict

update_video_use_case = partial(
    use_case,
    describe_videos_fn=describe,
    prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
    parse_video_into_state_dict_fn=parse_video_into_state_dict
)
