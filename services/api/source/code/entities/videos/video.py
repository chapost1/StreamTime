from entities.videos.uploaded_video import UploadedVideo
from pydantic import HttpUrl
from typing import Optional, List, Set, ClassVar
import datetime

# a list of required fields to update while listing the video for the first time
# otherwise, they will remain empty
REQUIRED_FIELDS_ON_LISTING = ['title', 'description']
# a set of fields which are allowed to update by design
ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS = {'title', 'description', 'is_private'}
ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING = ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS.union({'listing_time'})


class Video(UploadedVideo):
    # static
    REQUIRED_FIELDS_ON_LISTING: ClassVar[List[str]] = REQUIRED_FIELDS_ON_LISTING
    ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING: ClassVar[Set[str]] = ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING
    ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS: ClassVar[Set[str]] = ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS

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
    
    _pagination_index: Optional[int]
    _storage_object_key: Optional[str]
    _storage_thumbnail_key: Optional[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # privates
        self._pagination_index = kwargs.get('pagination_index', None)
        self._storage_object_key = kwargs.get('storage_object_key', None)
        self._storage_thumbnail_key = kwargs.get('storage_thumbnail_key', None)


    @property
    def pagination_index(self) -> str:
        return self._pagination_index


    @property
    def storage_object_key(self) -> str:
        return self._storage_object_key


    @property
    def storage_thumbnail_key(self) -> str:
        return self._storage_thumbnail_key

    
    def is_listed(self) -> bool:
        return self.listing_time is not None
    

    def is_not_listed(self) -> bool:
        return not self.is_listed()
