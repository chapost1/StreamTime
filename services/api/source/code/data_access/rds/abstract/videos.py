from typing import Protocol
from typing import List, Dict
from models import Video, UnprocessedVideo, SortKeys, VideoStages
from uuid import UUID

class VideosDbInterface(Protocol):
    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        """
        Find whether a video is actually exists or not
        - if not, it will be None
        - else, it will return it's current stage
        """

    async def get_listed_videos(self, allow_privates_of_user_id: UUID, exclude_user_id: UUID) -> List[Video]:
        """
        Gets listed videos
        - allows privates only for specific user_id (to support authenticated user)
        - supports the option to hide specific user_id (to let user explore others videos)
        """
    
    async def get_user_unprocessed_videos(self, user_id: str) -> List[UnprocessedVideo]:
        """
        Gets User Unprocess videos (failed or during processing)
        """
    
    async def get_user_videos(self, user_id: UUID, hide_private: bool, listed_only: bool, sort_key: SortKeys) -> List[UnprocessedVideo]:
        """
        Gets User videos
        - supports hiding listed/privates to protect user assets from unauthorized
        """
    
    async def get_video(self, user_id: UUID, hash_id: UUID) -> Video:
        """
        Get specific video
        """
    
    async def update_video(self, user_id: UUID, hash_id: UUID, to_update: Dict) -> None:
        """
        Update specific video (listed/allready processed one)
        """
