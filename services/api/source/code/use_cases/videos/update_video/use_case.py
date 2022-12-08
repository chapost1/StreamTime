from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.db_operation_utils.abstract import (
    SearchOneInDatabaseFunction,
    UpdateInDatabaseFunction
)
from use_cases.videos.update_video.abstract_internals import (
    SearchableUpdatable,
    DescribeVideosInDatabaseFunction,
    PrepareNewListingBeforePublishFunction,
    PrepareListedRecordBeforeUpdateFunction,
    ParseVideoIntoStateDictFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_one_in_database_fn: SearchOneInDatabaseFunction,
    update_in_database_fn: UpdateInDatabaseFunction,
    describe_videos_in_database_fn: DescribeVideosInDatabaseFunction,
    prepare_new_listing_before_publish_fn: PrepareNewListingBeforePublishFunction,
    prepare_listed_record_before_update_fn: PrepareListedRecordBeforeUpdateFunction,
    parse_video_into_state_dict_fn: ParseVideoIntoStateDictFunction,
    # usage scope
    authenticated_user_id: UUID,
    video: Video,
    hash_id: UUID
) -> None:
    """Updates an existing video"""

    # TODO: support new thumbnail selection

    db_videos_describer: SearchableUpdatable = describe_videos_in_database_fn(
        database=database,
        authenticated_user_id=authenticated_user_id,
        hash_id=hash_id
    )

    existing_video: Video = await search_one_in_database_fn(
        searchable=db_videos_describer
    )

    if existing_video.is_not_listed():
        video = prepare_new_listing_before_publish_fn(video=video)
    else:
        video = prepare_listed_record_before_update_fn(video=video)

    await update_in_database_fn(
        updatable=db_videos_describer,
        new_desired_state=parse_video_into_state_dict_fn(
            video=video
        )
    )
