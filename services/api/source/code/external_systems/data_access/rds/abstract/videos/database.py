from typing import Protocol, List, Dict, Tuple, Optional
from entities.videos import VideoStages, Video, UnprocessedVideo
from uuid import UUID


class VideosDatabase(Protocol):
    """VideosDatabase database class protocol"""


    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        """
        Find whether a video is actually exists or not
        - if not, it will be None
        - else, it will return it's current stage
        """


    async def get_videos(
        self,
        user_id: Optional[UUID],
        hash_id: Optional[UUID],
        not_user_id: Optional[UUID],
        include_privates_of_user_id: Optional[UUID],
        filter_unlisted: Optional[bool],
        next: Optional[str],
        page_limit: Optional[int]
    ) -> Tuple[List[Video], str]:
        """
        Gets a page of videos
        """
    

    async def update_video(
        self,
        user_id: UUID,
        hash_id: UUID,
        new_desired_state: Dict
    ) -> None:
        """
        Updates video of specified user if exits
        """


    async def delete_video(
        self,
        user_id: UUID,
        hash_id: UUID,
    ) -> None:
        """
        Deletes a video of specified user if exists
        """


    async def get_unprocessed_videos(
        self,
        user_id: Optional[UUID],
        hash_id: Optional[UUID]
    ) -> List[UnprocessedVideo]:
        """
        Gets unprocessed videos
        """


    async def delete_unprocessed_video(
        self,
        user_id: UUID,
        hash_id: UUID,
    ) -> None:
        """
        Deletes an unprocessed video of specified user if exists
        """
