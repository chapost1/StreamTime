from __future__ import annotations
from typing import Protocol, List, Dict
from entities.videos import Video
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.describers.described_uploaded_videos import DescribedUploadedVideos


class DescribedVideos(DescribedUploadedVideos, Protocol):
    """Videos database class protocol"""

    # searchable
    async def search(self) -> List[Video]:
        """Searches videos according to the applied conditions"""
    
    # deletable
    async def delete(self) -> None:
        """Deletes videos according to the applied conditions"""
    
    # updatable
    async def update(self, to_update: Dict) -> None:
        """Updates videos according to the applied conditions"""

    # override to support abstract return of self
    def with_hash(self, id: UUID) -> DescribedVideos:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def owned_by(self, user_id: UUID) -> DescribedVideos:
        """Restricts videos owner (user)"""

    def not_owned_by(self, user_id: UUID) -> DescribedVideos:
        """Filters out videos of certain user"""

    def include_privates_of(self, user_id: UUID) -> DescribedVideos:
        """Inlcudes privates of specific user"""

    def filter_unlisted(self, flag: bool = True) -> DescribedVideos:
        """Filters out any unlisted videos"""

    def filter_privates(self, flag: bool = True) -> DescribedVideos:
        """Filters out any private videos"""

    def paginate(self, pagination_index_is_smaller_than: int) -> DescribedVideos:
        """Sets pagination setting (next factor only)"""
    
    def limit(self, limit: int) -> DescribedVideos:
        """Limits the returned amount of videos"""
