from typing import Protocol
from typing import Dict
from entities.videos import VideoStages
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.videos_explorer import VideosExplorer
from external_systems.data_access.rds.abstract.videos.unprocessed_videos_explorer import UnprocessedVideosExplorer


class VideosDB(Protocol):
    """Videos database class protocol"""

    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        """
        Find whether a video is actually exists or not
        - if not, it will be None
        - else, it will return it's current stage
        """


    def videos(self) -> VideosExplorer:
        """
        Gets new instance of videos explorer
        """


    def unprocessd_videos(self) -> UnprocessedVideosExplorer:
        """
        Gets new instance of unprocessed videos explorer
        """


    async def update_video(self, user_id: UUID, hash_id: UUID, to_update: Dict) -> None:
        """
        Update specific video (listed/allready processed one)
        """


    async def delete_video_by_stage(self, user_id: UUID, hash_id: UUID, stage: VideoStages) -> NotImplementedError:
        """
        Removes a video record from the right table, by stage
        """
