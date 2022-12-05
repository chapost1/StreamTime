from entities.videos import UserVideosList
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from uuid import UUID
from typing import Protocol
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)
from common.utils import run_in_parallel
from use_cases.db_operation_utils.abstract import SearchDbFn


class DescribeUnprocessedVideosFn(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        authenticated_user_id: UUID
    ) -> Searchable:
        ...


class DescribeVideosFn(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        authenticated_user_id: UUID
    ) -> Searchable:
        ...


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_db_fn: SearchDbFn,
    describe_unprocessed_videos_fn: DescribeUnprocessedVideosFn,
    describe_videos_fn: DescribeVideosFn,
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
            searchable=describe_unprocessed_videos_fn(
                database=database,
                authenticated_user_id=authenticated_user_id
            )
        ),
        search_db_fn(
            searchable=describe_videos_fn(
                database=database,
                authenticated_user_id=authenticated_user_id
            )
        )
    )

    return UserVideosList(
        unprocessed_videos=unprocessed_videos,
        videos=videos
    )
