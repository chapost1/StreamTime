from typing import Dict
from uuid import UUID
from data_access.abstract import VideosDB

def make_get_upload_url(videos: VideosDB):
    async def get_upload_url(authenticated_user_id: UUID) -> Dict:
        # use videosdb to verify created uuid is not used for particular user
        """todo: implement""" # create hash_id and presigned url on s3 (needs the bucket name)

    return get_upload_url
