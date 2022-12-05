from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from common.utils import find_one
from use_cases.db_operation_utils.abstract import (
    SearchDbFn,
    UpdateDbFn
)
from use_cases.videos.update_video.abstract_internals import (
    SearchableUpdatable,
    DescribeDbVideosFn,
    PrepareNewListingBeforePublishFn,
    ParseVideoIntoStateDictFn
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_db_fn: SearchDbFn,
    update_db_fn: UpdateDbFn,
    describe_db_videos_fn: DescribeDbVideosFn,
    prepare_new_listing_before_publish_fn: PrepareNewListingBeforePublishFn,
    parse_video_into_state_dict_fn: ParseVideoIntoStateDictFn,
    # usage scope
    authenticated_user_id: UUID,
    video: Video,
    hash_id: UUID
) -> None:
    """Updates an existing video"""

    # TODO: support new thumbnail selection

    db_videos_describer: SearchableUpdatable = describe_db_videos_fn(
        database=database,
        authenticated_user_id=authenticated_user_id,
        hash_id=hash_id
    )

    existing_video: Video = find_one(
        items=await search_db_fn(searchable=db_videos_describer)
    )

    is_not_listed = not existing_video.is_listed()
    if is_not_listed:
        video = prepare_new_listing_before_publish_fn(video=video)

    await update_db_fn(
        updatable=db_videos_describer,
        new_desired_state=parse_video_into_state_dict_fn(
            video=video
        )
    )
