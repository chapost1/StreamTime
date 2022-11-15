from uuid import UUID
from typing import Callable
from data_access.rds.abstract import VideosDB
from common.app_errors import NotFoundError, TooEarlyError
from models.videos import VideoStages, Video, UnprocessedVideo
from data_access.storage.abstract import Storage

def make_delete_video_on_ready_stage_hadler(videos: VideosDB, storage: Storage) -> Callable[[UUID, UUID], None]:
  async def delete_video_on_ready_stage_hadler(user_id: UUID, hash_id: UUID) -> None:
    # get video meta for delete from S3 in case it is already preoccessed
    video: Video = await videos.get_video(user_id=user_id, hash_id=hash_id)
    # first remove the video so in case of failure, at max the user won't have access to corrupted video record
    # and another service may collect removed records and handle cleaning it up
    await videos.delete_video_by_stage(
      user_id=user_id,
      hash_id=hash_id,
      stage=VideoStages.READY.value
    )
    # delete from S3 [both video and thumbnail]
    await storage.delete_file(video._storage_object_key)
    await storage.delete_file(video._storage_thumbnail_key)
  return delete_video_on_ready_stage_hadler

def make_delete_unprocessed_video_handler(videos: VideosDB) -> Callable[[UUID, UUID], None]:
  async def delete_unprocessed_video_handler(user_id: UUID, hash_id: UUID) -> None:
    video: UnprocessedVideo = await videos.get_unprocessed_video(user_id=user_id, hash_id=hash_id)

    if video.is_still_processing():
      raise TooEarlyError()
    
    await videos.delete_video_by_stage(
      user_id=user_id,
      hash_id=hash_id,
      stage=VideoStages.UNPROCESSED.value
    )
  return delete_unprocessed_video_handler


def make_delete_video(videos: VideosDB, storage: Storage) -> Callable[[UUID, UUID], None]:
  delete_action_by_stage = {
    VideoStages.UNPROCESSED.value: make_delete_unprocessed_video_handler(videos=videos),
    VideoStages.READY.value: make_delete_video_on_ready_stage_hadler(videos=videos, storage=storage),
  }
  async def delete_video(authenticated_user_id: UUID, hash_id: UUID) -> None:
    # verify video / unprocessed_video
    video_stages = await videos.find_video_stage(user_id=authenticated_user_id, hash_id=hash_id)
    if video_stages is None:
      raise NotFoundError()

    for stage in video_stages:
      if stage in delete_action_by_stage:
        delete: Callable[[UUID, UUID], None] = delete_action_by_stage.get(stage)
        await delete(user_id=authenticated_user_id, hash_id=hash_id)

  return delete_video
