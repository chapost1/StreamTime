from entities.videos import UserVideosList
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from uuid import UUID
from common.utils import run_in_parallel
from use_cases.db_operation_utils.abstract import SearchDbFn
from use_cases.videos.get_authenticated_user_videos.abstract_internals import (
    DescribeDbUnprocessedVideosFn,
    DescribeDbVideosFn
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_db_fn: SearchDbFn,
    describe_db_unprocessed_videos_fn: DescribeDbUnprocessedVideosFn,
    describe_db_videos_fn: DescribeDbVideosFn,
    # usage scope
    authenticated_user_id: UUID
) -> UserVideosList:
    """
    Gets Authenticated User Videos

    This action is usually relevant when user wants to list it's uploaded videos state
    For example, after uploading a video, user will want to update it and then publish
    """

    # TODO: USE & support pagination as an external param for ready videos

    unprocessed_videos, videos = await run_in_parallel(
        search_db_fn(
            searchable=describe_db_unprocessed_videos_fn(
                database=database,
                authenticated_user_id=authenticated_user_id
            )
        ),
        search_db_fn(
            searchable=describe_db_videos_fn(
                database=database,
                authenticated_user_id=authenticated_user_id
            )
        )
    )

    return UserVideosList(
        unprocessed_videos=unprocessed_videos,
        videos=videos
    )
