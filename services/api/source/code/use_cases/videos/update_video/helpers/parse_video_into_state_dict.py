from entities.videos import Video
from typing import Dict


def parse_video_into_state_dict(
    video: Video
) -> Dict:
    # filter-in allowed update fields, to avoid update of forbidden fields
    return video.dict(include=Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING, exclude_none=True)
