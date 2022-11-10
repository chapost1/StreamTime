from dataclasses import dataclass
from typing import List
from models.videos.unprocessed_video import UnprocessedVideo
from models.videos.video import Video


@dataclass
class UserVideosList:
    unprocessed_videos: List[UnprocessedVideo]
    videos: List[Video]
