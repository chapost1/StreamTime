from entities.videos import UserVideosList
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from uuid import UUID
from common.utils import run_in_parallel


async def use_case(
    # creation scope
    database: VideosDatabase,
    # usage scope
    authenticated_user_id: UUID
) -> UserVideosList:
    """
    Gets Authenticated User Videos

    This action is usually relevant when user wants to list it's uploaded videos state
    For example, after uploading a video, user will want to update it and then publish
    """

    unprocessed_videos, videos_page = await run_in_parallel(
        database.get_unprocessed_videos(
            include_user_id=authenticated_user_id
        ),
        database.get_videos(
            include_user_id=authenticated_user_id,
            filter_unlisted=False,
            include_privates_of_user_id=authenticated_user_id
        )
    )

    # TODO: USE & support pagination as an external param for videos
    videos, _ = videos_page

    return UserVideosList(
        unprocessed_videos=unprocessed_videos,
        videos=videos
    )
