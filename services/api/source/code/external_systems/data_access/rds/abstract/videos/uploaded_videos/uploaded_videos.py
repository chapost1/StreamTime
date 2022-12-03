from __future__ import annotations
from typing import Protocol
from uuid import UUID


class UploadedVideos(Protocol):
    """UploadedVideos database class protocol"""

    @property
    def hash_id(self) -> UUID:
        pass


    @property
    def video_id(self) -> UUID:
        pass


    def with_id(self, id: UUID) -> UploadedVideos:
        """Restricts video hash_id"""


    def of_user(self, user_id: UUID) -> UploadedVideos:
        """Restricts videos owner (user)"""

