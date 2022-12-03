from __future__ import annotations
from typing import Protocol
from uuid import UUID


class UploadedVideosDescriber(Protocol):
    """
    UploadedVideosDescriber database class protocol
    Its purpose is to describe video entities
    so later data manipulations/query will work on the described videos
    """

    @property
    def hash_id(self) -> UUID:
        pass


    @property
    def video_id(self) -> UUID:
        pass


    def with_hash(self, id: UUID) -> UploadedVideosDescriber:
        """Restricts video hash_id"""


    def owned_by(self, user_id: UUID) -> UploadedVideosDescriber:
        """Restricts videos owner (user)"""

