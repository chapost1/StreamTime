from models.videos.uploaded_video import UploadedVideo
from pydantic import HttpUrl
from typing import Optional
import datetime


class Video(UploadedVideo):
    title: Optional[str]
    description: Optional[str]
    size_in_bytes: Optional[int]
    duration_seconds: Optional[int]
    video_type: Optional[str]
    thumbnail_url: Optional[HttpUrl]
    is_private: Optional[bool]
    listing_time: Optional[datetime.datetime]
    
    def is_listed(self) -> bool:
        return self.listing_time is not None
