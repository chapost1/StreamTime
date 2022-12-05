from pydantic import BaseModel
from typing import List
from entities.videos.unprocessed_video import UnprocessedVideo
from entities.videos.video import Video


class UserVideosList(BaseModel):
    unprocessed_videos: List[UnprocessedVideo]
    videos: List[Video]
