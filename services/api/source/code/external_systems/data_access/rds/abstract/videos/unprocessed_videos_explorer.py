from __future__ import annotations
from typing import Protocol, List
from entities.videos import UnprocessedVideo
from uuid import UUID


class UnprocessedVideosExplorer(Protocol):
    """UnprocessedVideosExplorer database class protocol"""

    async def search(self) -> List[UnprocessedVideo]:
        """Searches unprocessed videos according to the applied conditions"""
    

    def id(self, id: UUID) -> UnprocessedVideosExplorer:
        """Restricts video hash_id"""


    def of_user(self, user_id: UUID) -> UnprocessedVideosExplorer:
        """Restricts videos owner (user)"""
