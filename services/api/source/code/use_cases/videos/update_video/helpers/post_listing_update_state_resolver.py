from use_cases.validation_utils.concrete import fail_on_unsupported_fields
from use_cases.videos.update_video.helpers.parse_video_into_state_dict import parse_video_into_state_dict
from entities.videos import Video
from typing import Dict


def resolve_update_state(video: Video) -> Dict:
    # assert listed video do not have anything which is unsupported for modification
    fail_on_unsupported_fields(
        entity=video.dict(exclude_none=True),
        supported_fields=Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS
    )

    # omits extra immutable fields
    return parse_video_into_state_dict(
        video=video,
        include_fields=Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS
    )
