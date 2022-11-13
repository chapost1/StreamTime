from models import Video
from uuid import UUID
from data_access.rds.abstract import VideosDB
from common.app_errors import NotFoundError
from models.videos import VideoStages
from data_access.storage.abstract import Storage


def make_delete_video(videos: VideosDB, storage: Storage):
    async def delete_video(authenticated_user_id: UUID, hash_id: UUID) -> None:
      # verify video / unprocessed_video
      video_stages = await videos.find_video_stage(user_id=authenticated_user_id, hash_id=hash_id)
      if video_stages is None:
        raise NotFoundError()

      for stage in video_stages:
        if stage != VideoStages.READY.value:
          # delete video from appropriate table
          return await videos.delete_video_by_stage(
            user_id=authenticated_user_id,
            hash_id=hash_id,
            stage=stage
          )
        
        # get video meta for delete from S3 in case it is already preoccessed
        video: Video = await videos.get_video(user_id=authenticated_user_id, hash_id=hash_id)
        # first remove the video so in case of failure, at max the user won't have access to corrupted video record
        # and another service may collect removed records and handle cleaning it up
        await videos.delete_video_by_stage(
          user_id=authenticated_user_id,
          hash_id=hash_id,
          stage=stage
        )
        # delete from S3 [both video and thumbnail]
        await storage.delete_file(video._storage_object_key)
        await storage.delete_file(video._storage_thumbnail_key)

    return delete_video
