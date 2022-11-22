from dataclasses import dataclass
from typing import List
from entities.videos.unprocessed_video import UnprocessedVideo
from entities.videos.video import Video


@dataclass
class UserVideosList:
    unprocessed_videos: List[UnprocessedVideo]
    videos: List[Video]
