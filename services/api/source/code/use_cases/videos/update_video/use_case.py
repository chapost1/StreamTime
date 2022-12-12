from uuid import UUID
from entities.videos import Video
from common.utils import first_item
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.videos.update_video.helpers.abstract import (
    ResolveUpdateStateForPreListingFunction,
    ResolveUpdateStateForPostListingFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    resolve_update_state_for_pre_listing_fn: ResolveUpdateStateForPreListingFunction,
    resolve_update_state_for_post_listing_fn: ResolveUpdateStateForPostListingFunction,
    # usage scope
    authenticated_user_id: UUID,
    video: Video,
    hash_id: UUID
) -> None:
    """Updates an existing video"""

    # TODO: support new thumbnail selection

    videos, _ = await database.get_videos(
        user_id=authenticated_user_id,
        hash_id=hash_id,
        filter_unlisted=False,
        include_privates_of_user_id=authenticated_user_id
    )

    existing_video: Video = first_item(
        items=videos
    )

    if existing_video.is_not_listed():
        desired_state = resolve_update_state_for_pre_listing_fn(video=video)
    else:
        desired_state = resolve_update_state_for_post_listing_fn(video=video)

    await database.update_video(
        user_id=authenticated_user_id,
        hash_id=hash_id,
        new_desired_state=desired_state
    )
