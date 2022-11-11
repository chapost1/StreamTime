from models import UserVideosList, SortKeys
from data_access.rds.abstract import VideosDB
from uuid import UUID

def make_get_authenticated_user_videos(videos: VideosDB):
    async def get_authenticated_user_videos(authenticated_user_id: UUID) -> UserVideosList:
        return UserVideosList(
            unprocessed_videos=await videos.get_user_unprocessed_videos(user_id=authenticated_user_id),
            videos=await videos.get_user_videos(
                user_id=authenticated_user_id,
                hide_private=False,
                listed_only=False,
                sort_key=SortKeys.upload_time
            )
        )
    return get_authenticated_user_videos
