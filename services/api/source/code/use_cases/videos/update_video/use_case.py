from uuid import UUID
from entities.videos import Video
from common.utils import find_one
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.videos.update_video.helpers.abstract import (
    PrepareNewListingBeforePublishFunction,
    PrepareListedRecordBeforeUpdateFunction,
    ParseVideoIntoStateDictFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
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

    videos, _ = await database.get_videos(
        include_user_id=authenticated_user_id,
        include_hash_id=hash_id,
        filter_unlisted=False,
        include_privates_of_user_id=authenticated_user_id
    )

    existing_video: Video = find_one(
        items=videos
    )

    if existing_video.is_not_listed():
        video = prepare_new_listing_before_publish_fn(video=video)
    else:
        video = prepare_listed_record_before_update_fn(video=video)

    new_desired_state = parse_video_into_state_dict_fn(
        video=video
    )

    await database.update_video(
        user_id=authenticated_user_id,
        hash_id=hash_id,
        new_desired_state=new_desired_state
    )
