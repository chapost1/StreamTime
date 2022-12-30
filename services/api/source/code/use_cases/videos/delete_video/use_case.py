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
    # validates existence
    first_item(
        items=await database.get_videos(
            user_id=user_id,
            filter_unlisted=False,
            hash_id=hash_id,
            include_privates_of_user_id=user_id
        )
    )

    await database.delete_video(
      user_id=user_id,
      hash_id=hash_id
    )


async def delete_unprocessed_video_handler(database: VideosDatabase, user_id: UUID, hash_id: UUID) -> None:
    """Marks a UnprocessedVideo as deleted on database"""

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

    tasks: List[Awaitable] = []

    for stage in video_stages:
      if stage in delete_action_by_stage:
        delete_action: Callable[[UUID, UUID], None] = delete_action_by_stage.get(stage)
        tasks.append(
          delete_action(
            database=database,
            user_id=authenticated_user_id,
            hash_id=hash_id
          )
        )
  
    await run_in_parallel(*tasks)
