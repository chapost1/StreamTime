from __future__ import annotations
from typing import Protocol, List
from entities.videos import UnprocessedVideo
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.uploaded_videos import UploadedVideos


class UnprocessedVideos(UploadedVideos, Protocol):
    """UnprocessedVideos database class protocol"""

    # searchable
    async def search(self) -> List[UnprocessedVideo]:
        """Searches unprocessed videos according to the applied conditions"""
    
    # deletable
    async def delete(self) -> None:
        """Deletes unprocessed videos according to the applied conditions"""

    # override to support abstract return of self
    def with_hash(self, id: UUID) -> UnprocessedVideos:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def owned_by(self, user_id: UUID) -> UnprocessedVideos:
        """Restricts videos owner (user)"""
