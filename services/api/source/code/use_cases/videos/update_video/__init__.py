from functools import partial
from .use_case import use_case
from .helpers import (
    prepare_new_listing_before_publish,
    prepare_listed_record_before_update,
    parse_video_into_state_dict
)


update_video_use_case = partial(
    use_case,
    prepare_new_listing_before_publish_fn=prepare_new_listing_before_publish,
    prepare_listed_record_before_update_fn=prepare_listed_record_before_update,
    parse_video_into_state_dict_fn=parse_video_into_state_dict
)
