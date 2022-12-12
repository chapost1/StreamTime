from use_cases.videos.update_video.helpers.parse_video_into_state_dict import parse_video_into_state_dict
from use_cases.validation_utils.concrete import (
    fail_on_unsupported_fields,
    assert_required_fields
)
from typing import Dict
from entities.videos import Video
from common.utils import calc_server_time


def resolve_update_state(video: Video) -> Dict:
    entity = video.dict(exclude_none=True)
    # assert new listing do not have anything which is unsupported for modification
    fail_on_unsupported_fields(
        entity=entity,
        supported_fields=Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING
    )

    # assert new listing has required fields
    assert_required_fields(
        entity=video.dict(exclude_none=True),
        fields=Video.REQUIRED_FIELDS_ON_LISTING
    )
    # avoid side effects
    replica = video.copy()
    # attach server time as listing time
    replica.listing_time = calc_server_time()

    # omits extra immutable fields
    return parse_video_into_state_dict(
        video=replica,
        include_fields=Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING
    )
