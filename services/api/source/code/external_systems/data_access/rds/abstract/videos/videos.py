from __future__ import annotations
from typing import Protocol, List, Dict
from entities.videos import Video
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.uploaded_videos import UploadedVideos


class Videos(UploadedVideos, Protocol):
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
    def with_id(self, id: UUID) -> Videos:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def of_user(self, user_id: UUID) -> Videos:
        """Restricts videos owner (user)"""

    def exclude_user(self, user_id: UUID) -> Videos:
        """Hides videos of certain user"""

    def allow_privates_of(self, user_id: UUID) -> Videos:
        """Allows privates of specific user"""

    def paginate(self, pagination_index_is_smaller_than: int) -> Videos:
        """Sets pagination setting (next factor only)"""
    
    def limit(self, limit: int) -> Videos:
        """Limits the returned amount of videos"""

    def hide_unlisted(self, flag: bool = True) -> Videos:
        """Hides any unlisted videos"""

    def hide_privates(self, flag: bool = True) -> Videos:
        """Hides any private videos"""
