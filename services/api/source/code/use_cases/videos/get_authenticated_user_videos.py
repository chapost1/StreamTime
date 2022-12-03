from entities.videos import UserVideosList
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from uuid import UUID
from typing import Callable
from common.utils import run_in_parallel


def make_get_authenticated_user_videos(database: VideosDatabase) -> Callable[[UUID], UserVideosList]:
    """Creates Get Authenticated User Videos use case"""

    async def get_authenticated_user_videos(authenticated_user_id: UUID) -> UserVideosList:
        """
        Gets Authenticated User Videos

        This action is usually relevant when user wants to list it's uploaded videos state
        For example, after uploading a video, user will want to update it and then publish
        """

        unprocessed_videos, videos = await run_in_parallel(
            database.describe_unprocessd_videos()
            .owned_by(user_id=authenticated_user_id)
            .search(),
            # TODO: USE & support pagination as an external param
            database.describe_videos()
            .owned_by(user_id=authenticated_user_id)
            .include_privates_of(user_id=authenticated_user_id)
            .search()
        )

        return UserVideosList(
            unprocessed_videos=unprocessed_videos,
            videos=videos
        )

    return get_authenticated_user_videos
