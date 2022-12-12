from entities.videos import Video
from typing import Dict, List


def parse_video_into_state_dict(
    video: Video,
    include_fields=List[str]
) -> Dict:
    # filter-in allowed update fields, to avoid update of forbidden fields
    return video.dict(include=set(include_fields), exclude_none=True)
