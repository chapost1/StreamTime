from functools import partial
from .use_case import use_case
from .helpers import (
    resolve_update_state_for_pre_listing,
    resolve_update_state_for_post_listing
)


update_video_use_case = partial(
    use_case,
    resolve_update_state_for_pre_listing_fn=resolve_update_state_for_pre_listing,
    resolve_update_state_for_post_listing_fn=resolve_update_state_for_post_listing
)
