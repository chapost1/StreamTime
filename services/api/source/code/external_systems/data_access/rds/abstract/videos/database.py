from typing import Protocol
from entities.videos import VideoStages
from uuid import UUID
from external_systems.data_access.rds.abstract.videos.describers import VideosDescriber
from external_systems.data_access.rds.abstract.videos.describers import UnprocessedVideosDescriber


class VideosDatabase(Protocol):
    """VideosDatabase database class protocol"""

    async def find_video_stage(self, user_id: UUID, hash_id: UUID) -> VideoStages:
        """
        Find whether a video is actually exists or not
        - if not, it will be None
        - else, it will return it's current stage
        """

    def describe_videos(self) -> VideosDescriber:
        """
        Gets new instance of videos describer
        """

    def describe_unprocessd_videos(self) -> UnprocessedVideosDescriber:
        """
        Gets new instance of unprocessed videos describer
        """
