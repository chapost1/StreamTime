from __future__ import annotations
from typing import Protocol, List
from entities.videos import UnprocessedVideo
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.describers.described_uploaded_videos import DescribedUploadedVideos


class DescribedUnprocessedVideos(DescribedUploadedVideos, Protocol):
    """DescribedUnprocessedVideos database class protocol"""

    # searchable
    async def search(self) -> List[UnprocessedVideo]:
        """Searches unprocessed videos according to the applied conditions"""
    
    # deletable
    async def delete(self) -> None:
        """Deletes unprocessed videos according to the applied conditions"""

    # override to support abstract return of self
    def with_hash(self, id: UUID) -> DescribedUnprocessedVideos:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def owned_by(self, user_id: UUID) -> DescribedUnprocessedVideos:
        """Restricts videos owner (user)"""
