from __future__ import annotations
from typing import Protocol, List
from entities.videos import UnprocessedVideo
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.describers.uploaded_videos import UploadedVideosDescriber


class UnprocessedVideosDescriber(UploadedVideosDescriber, Protocol):
    """
    UnprocessedVideosDescriber database class protocol
    Its purpose is to describe unprocessed video entities
    so later data manipulations/query will work on the described videos
    """

    # searchable
    async def search(self) -> List[UnprocessedVideo]:
        """Searches unprocessed videos according to the applied conditions"""
    
    # deletable
    async def delete(self) -> None:
        """Deletes unprocessed videos according to the applied conditions"""

    # override to support abstract return of self
    def with_hash(self, id: UUID) -> UnprocessedVideosDescriber:
        """Restricts video hash_id"""

    # override to support abstract return of self
    def owned_by(self, user_id: UUID) -> UnprocessedVideosDescriber:
        """Restricts videos owner (user)"""
