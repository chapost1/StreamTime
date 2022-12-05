from use_cases.validation_utils import assert_required_fields
from entities.videos import Video
from common.utils import calc_server_time


def prepare_new_listing_before_publish(video: Video) -> Video:
    # assert new listing has required fields
    assert_required_fields(video.dict(exclude_none=True), Video.REQUIRED_FIELDS_ON_LISTING)
    # avoid side effects
    replica = video.copy()
    # attach server time as listing time
    replica.listing_time = calc_server_time()

    return replica
