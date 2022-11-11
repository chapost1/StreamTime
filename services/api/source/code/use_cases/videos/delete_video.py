from models import Video
from uuid import UUID
from data_access.rds.abstract import VideosDB

def make_delete_video(videos: VideosDB):
    async def delete_video(authenticated_user_id: UUID, hash_id: UUID) -> None:
      # verify video / unprocessed_video
      # delete video from appropriate table
      # here, user can already recieve 200 OK
      # delete from S3 [both video and thumbnail]
      """todo: implement"""

    return delete_video
