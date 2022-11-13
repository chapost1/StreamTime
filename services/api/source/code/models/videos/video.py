from models.videos.uploaded_video import UploadedVideo
from pydantic import HttpUrl, Field
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
    class Config:
        underscore_attrs_are_private = True
    
    _storage_object_key: Optional[str]
    _storage_thumbnail_key: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._storage_object_key = kwargs.get('_storage_object_key', None)
        self._storage_thumbnail_key = kwargs.get('_storage_thumbnail_key', None)

    
    def is_listed(self) -> bool:
        return self.listing_time is not None
