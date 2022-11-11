from typing import List, Union
from uuid import UUID
from models import Video, SortKeys
from data_access.rds.abstract import VideosDB

# get specific user videos
def make_get_specific_user_videos(videos: VideosDB):
    async def get_specific_user_videos(authenticated_user_id: Union[UUID, str], user_id: UUID) -> List[Video]:
        # build visibility settings by matching selected user id to the viewer
        if authenticated_user_id.__eq__(user_id):
            hide_private = False
            listed_only = False
            sort_key = SortKeys.upload_time
        else:
            hide_private = True
            listed_only = True
            sort_key = SortKeys.listing_time

        return await videos.get_user_videos(
            user_id=user_id,
            hide_private=hide_private,
            listed_only=listed_only,
            sort_key=sort_key
        )

    return get_specific_user_videos
