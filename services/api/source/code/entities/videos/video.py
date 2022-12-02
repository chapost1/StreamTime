from entities.videos.uploaded_video import UploadedVideo
from pydantic import HttpUrl
from typing import Optional, List, Set, ClassVar
import datetime

# a list of required fields to update while listing the video for the first time
# otherwise, they will remain empty
REQUIRED_FIELDS_ON_LISTING = ['title', 'description']
# a set of fields which are allowed to update by design
ALLOWED_UPDATE_FIELDS = {'title', 'description', 'listing_time', 'is_private'}

class Video(UploadedVideo):
    # static
    REQUIRED_FIELDS_ON_LISTING: ClassVar[List[str]] = REQUIRED_FIELDS_ON_LISTING
    ALLOWED_UPDATE_FIELDS: ClassVar[Set[str]] = ALLOWED_UPDATE_FIELDS

    # per instance
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
