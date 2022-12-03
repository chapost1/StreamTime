from __future__ import annotations
from typing import Protocol, List
from entities.videos import Video
from uuid import UUID


class VideosExplorer(Protocol):
    """VideosExplorer database class protocol"""

    async def search(self) -> List[Video]:
        """Searches videos according to the applied conditions"""
    

    def id(self, id: UUID) -> VideosExplorer:
        """Restricts video hash_id"""


    def of_user(self, user_id: UUID) -> VideosExplorer:
        """Restricts videos owner (user)"""
    

    def exclude_user(self, user_id: UUID) -> VideosExplorer:
        """Hides videos of certain user"""


    def allow_privates_of(self, user_id: UUID) -> VideosExplorer:
        """Allows privates of specific user"""


    def paginate(self, pagination_index_is_smaller_than: int) -> VideosExplorer:
        """Sets pagination setting (next factor only)"""
    

    def limit(self, limit: int) -> VideosExplorer:
        """Limits the returned amount of videos"""


    def hide_unlisted(self, flag: bool = True) -> VideosExplorer:
        """Hides any unlisted videos"""


    def hide_privates(self, flag: bool = True) -> VideosExplorer:
        """Hides any private videos"""
