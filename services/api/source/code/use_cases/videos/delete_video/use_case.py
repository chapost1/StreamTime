from uuid import UUID
from typing import Callable, List, Awaitable
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from common.app_errors import NotFoundError, TooEarlyError
from entities.videos import VideoStages, Video, UnprocessedVideo
from external_systems.data_access.storage.abstract import Storage
from common.utils import (
  run_in_parallel,
  find_one
)


def make_delete_video_on_ready_stage_handler(database: VideosDatabase, storage: Storage) -> Callable[[UUID, UUID], None]:
  """Creates Delete a ready state Video handler"""

  async def delete_video_on_ready_stage_hadnler(user_id: UUID, hash_id: UUID) -> None:
    """Deletes a ready state Video from database and also it's assets from storage"""

    # first, get video meta to delete assets from storage
    videos, _ = await database.get_videos(
        include_user_id=user_id,
        filter_unlisted=False,
        include_hash_id=hash_id,
        include_privates_of_user_id=user_id
    )
    video: Video = find_one(
        items=videos
    )

    # then, remove the video so in case of failure, at max the user won't have access to corrupted video record
    # and another service may collect removed records and handle cleaning it up
    await database.delete_video(
      user_id=user_id,
      hash_id=hash_id
    )

    # delete from storage [both video and thumbnail]
    await storage.delete_file(item_relative_path=video.storage_object_key)
    await storage.delete_file(item_relative_path=video.storage_thumbnail_key)

  return delete_video_on_ready_stage_hadnler


def make_delete_unprocessed_video_handler(database: VideosDatabase) -> Callable[[UUID, UUID], None]:
  """Creates Delete an unprocessed Video handler"""

  async def delete_unprocessed_video_handler(user_id: UUID, hash_id: UUID) -> None:
    """Deletes an unprocessed Video from database"""

    unprocessed_video: UnprocessedVideo = find_one(
        items=await database.get_unprocessed_videos(
          include_user_id=user_id,
          include_hash_id=hash_id
        )
    )

    if unprocessed_video.is_still_processing():
      raise TooEarlyError()

    await database.delete_unprocessed_video(
      user_id=user_id,
      hash_id=hash_id
    )

  return delete_unprocessed_video_handler


def make_delete_video(database: VideosDatabase, storage: Storage) -> Callable[[UUID, UUID], None]:
    """Creates Delete Video use case"""

    # initialize delete actions and keep it as a closure in memory
    # TODO: remove complex delete actions when garbage collector service is ready
    # all the logic in here should be changed to only call 'mark as delete' instead of [finding, dealing with multi handle types]
    delete_action_by_stage = {
      VideoStages.UNPROCESSED.value: make_delete_unprocessed_video_handler(database=database),
      VideoStages.READY.value: make_delete_video_on_ready_stage_handler(database=database, storage=storage),
    }

    async def delete_video(authenticated_user_id: UUID, hash_id: UUID) -> None:
      """Deletes a Video forever"""

      # find in which stage the Video is at: video (ready) / unprocessed_video
      video_stages = await database.find_video_stage(user_id=authenticated_user_id, hash_id=hash_id)
      if video_stages is None:
        raise NotFoundError()

      tasks: List[Awaitable] = []

      for stage in video_stages:
        if stage in delete_action_by_stage:
          delete_action: Callable[[UUID, UUID], None] = delete_action_by_stage.get(stage)
          tasks.append(
            delete_action(user_id=authenticated_user_id, hash_id=hash_id)
          )
      
      await run_in_parallel(*tasks)

    return delete_video
