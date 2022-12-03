from typing import Protocol
from typing import List, Dict
from entities.videos import Video, UnprocessedVideo, VideoStages
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.videos_explorer import VideosExplorer


class VideosDB(Protocol):
    """Videos database class protocol"""

    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        """
        Find whether a video is actually exists or not
        - if not, it will be None
        - else, it will return it's current stage
        """


    def get_videos_explorer(self) -> VideosExplorer:
        """
        Gets new instance of videos explorer
        """


    async def get_user_unprocessed_videos(self, user_id: str) -> List[UnprocessedVideo]:
        """
        Gets User Unprocess videos (failed or during processing)
        """


    async def get_unprocessed_video(self, user_id: UUID, hash_id: UUID) -> UnprocessedVideo:
        """
        Get specific unprocessed video
        """


    async def update_video(self, user_id: UUID, hash_id: UUID, to_update: Dict) -> None:
        """
        Update specific video (listed/allready processed one)
        """


    async def delete_video_by_stage(self, user_id: UUID, hash_id: UUID, stage: VideoStages) -> NotImplementedError:
        """
        Removes a video record from the right table, by stage
        """
