from __future__ import annotations
from typing import Protocol
from uuid import UUID


class DescribedUploadedVideos(Protocol):
    """DescribedUploadedVideos database class protocol"""

    @property
    def hash_id(self) -> UUID:
        pass


    @property
    def video_id(self) -> UUID:
        pass


    def with_hash(self, id: UUID) -> DescribedUploadedVideos:
        """Restricts video hash_id"""


    def owned_by(self, user_id: UUID) -> DescribedUploadedVideos:
        """Restricts videos owner (user)"""

