from entities.videos import UserVideosList
from external_systems.data_access.rds.abstract.videos import VideosDB
from uuid import UUID
from typing import Callable
from common.utils import run_in_parallel


def make_get_authenticated_user_videos(database: VideosDB) -> Callable[[UUID], UserVideosList]:
    """Creates Get Authenticated User Videos use case"""

    async def get_authenticated_user_videos(authenticated_user_id: UUID) -> UserVideosList:
        """
        Gets Authenticated User Videos

        This action is usually relevant when user wants to list it's uploaded videos state
        For example, after uploading a video, user will want to update it and then publish
        """

        unprocessed_videos, videos = await run_in_parallel(
            database.get_user_unprocessed_videos(
                user_id=authenticated_user_id
            ),
            # TODO: USE & support pagination as an external param
            database.get_videos_explorer()
            .of_user(user_id=authenticated_user_id)
            .allow_privates_of(user_id=authenticated_user_id)
            .search()
        )

        return UserVideosList(
            unprocessed_videos=unprocessed_videos,
            videos=videos
        )

    return get_authenticated_user_videos
