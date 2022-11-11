from models import Video
from uuid import UUID
from data_access.abstract import VideosDB

def make_delete_video(videos: VideosDB):
    async def delete_video(authenticated_user_id: UUID, hash_id: UUID) -> None:
       """todo: implement""" # consider the case of hash_id in unprocessed / videos

    return delete_video
