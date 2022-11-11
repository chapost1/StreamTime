from uuid import UUID
from data_access.abstract import VideosDB
from typing import Union
from models import WatchVideoRecord

def make_get_watch_video_record(videos: VideosDB):
    async def get_watch_video_record(authenticated_user_id: Union[UUID, str], user_id: UUID, hash_id: UUID) -> WatchVideoRecord:
        """todo: implement""" # if not private / private but user has premissions, create presigned url on S3

    return get_watch_video_record
