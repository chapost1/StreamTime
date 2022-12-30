from uuid import UUID
from typing import Callable, List, Awaitable
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from common.app_errors import NotFoundError, TooEarlyError
from entities.videos import VideoStages, UnprocessedVideo
from common.utils import (
    run_in_parallel,
    first_item
)


async def delete_video_on_ready_stage_hadnler(database: VideosDatabase, user_id: UUID, hash_id: UUID) -> None:
    """Marks a Video as deleted on database"""
    # no need to validate existence as it is already done in find_video_stage
    await database.delete_video(
        user_id=user_id,
        hash_id=hash_id
    )


async def delete_unprocessed_video_handler(database: VideosDatabase, user_id: UUID, hash_id: UUID) -> None:
    """Marks a UnprocessedVideo as deleted on database"""

    # get the unprocessed_video to check if it is still processing
    unprocessed_video: UnprocessedVideo = first_item(
        items=await database.get_unprocessed_videos(
            user_id=user_id,
            hash_id=hash_id
        )
    )

    if unprocessed_video.is_still_processing():
        raise TooEarlyError()

    await database.delete_unprocessed_video(
        user_id=user_id,
        hash_id=hash_id
    )


delete_action_by_stage = {
    VideoStages.UNPROCESSED.value: delete_unprocessed_video_handler,
    VideoStages.READY.value: delete_video_on_ready_stage_hadnler,
}


async def use_case(
    # ceation scope
    database: VideosDatabase,
    # usage scope
    authenticated_user_id: UUID,
    hash_id: UUID
) -> None:
    """Marks a Video as deleted on database if it exists"""
    
    # find in which stage the Video is at: video (ready) / unprocessed_video
    video_stages = await database.find_video_stage(user_id=authenticated_user_id, hash_id=hash_id)
    if video_stages is None:
        raise NotFoundError()
    # validate that the stages are valid
    # this is a safety check as the database should only return valid stages
    # but it is better to be safe than sorry
    invalid_stages = set(video_stages) - set(delete_action_by_stage.keys())
    if invalid_stages:
        raise ValueError(f'Invalid stages: {invalid_stages}')

    tasks: List[Awaitable] = []

    for stage in video_stages:
        delete_action = delete_action_by_stage.get(stage)
        tasks.append(
            delete_action(
                database=database,
                user_id=authenticated_user_id,
                hash_id=hash_id
            )
        )
  
    await run_in_parallel(*tasks)
