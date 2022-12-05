from uuid import UUID
from typing import Protocol, Dict
from entities.videos import Video
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable,
    Updatable
)
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from common.utils import find_one
from use_cases.db_operation_utils.abstract import (
    SearchDbFn,
    UpdateDbFn
)


class SearchableUpdatable(Searchable, Updatable, Protocol):
    pass


class DescribeVideosFn(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        hash_id: UUID,
        authenticated_user_id: UUID
    ) -> SearchableUpdatable:
        ...


class PrepareNewListingBeforePublishFn(Protocol):
    def __call__(self, video: Video) -> Video: ...


class ParseVideoIntoStateDictFn(Protocol):
    def __call__(self, video: Video) -> Dict: ...


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_db_fn: SearchDbFn,
    update_db_fn: UpdateDbFn,
    describe_videos_fn: DescribeVideosFn,
    prepare_new_listing_before_publish_fn: PrepareNewListingBeforePublishFn,
    parse_video_into_state_dict_fn: ParseVideoIntoStateDictFn,
    # usage scope
    authenticated_user_id: UUID,
    video: Video,
    hash_id: UUID
) -> None:
    """Updates an existing video"""

    # TODO: support new thumbnail selection

    videos_describer: SearchableUpdatable = describe_videos_fn(
        database=database,
        authenticated_user_id=authenticated_user_id,
        hash_id=hash_id
    )

    existing_video: Video = find_one(
        items=await search_db_fn(searchable=videos_describer)
    )

    is_not_listed = not existing_video.is_listed()
    if is_not_listed:
        video = prepare_new_listing_before_publish_fn(video=video)

    await update_db_fn(
        updatable=videos_describer,
        new_desired_state=parse_video_into_state_dict_fn(
            video=video
        )
    )
