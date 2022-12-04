from __future__ import annotations
from typing import Protocol, List, Dict
from entities.videos import Video
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.describers.uploaded_videos import UploadedVideosDescriber


class VideosDescriber(UploadedVideosDescriber, Protocol):
    """
    VideosDescriber database class protocol
    Its purpose is to describe video entities
    so later data manipulations/query will work on the described videos
    """

    # searchable
    async def search(self) -> List[Video]:
        """Searches videos according to the applied conditions"""
    
    # deletable
    async def delete(self) -> None:
        """Deletes videos according to the applied conditions"""
    
    # updatable
    async def update(self, new_desired_state: Dict) -> None:
        """Updates videos according to the applied conditions"""

    # override to support abstract return of self
    def with_hash(self, id: UUID) -> VideosDescriber:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def owned_by(self, user_id: UUID) -> VideosDescriber:
        """Restricts videos owner (user)"""

    def not_owned_by(self, user_id: UUID) -> VideosDescriber:
        """Filters out videos of certain user"""

    def include_privates_of(self, user_id: UUID) -> VideosDescriber:
        """Inlcudes privates of specific user"""

    def filter_unlisted(self, flag: bool = True) -> VideosDescriber:
        """Filters out any unlisted videos"""

    def unfilter_privates(self, flag: bool = True) -> VideosDescriber:
        """Filters out any private videos"""

    def paginate(self, pagination_index_is_smaller_than: int) -> VideosDescriber:
        """Sets pagination setting (next factor only)"""
    
    def limit(self, limit: int) -> VideosDescriber:
        """Limits the returned amount of videos"""
