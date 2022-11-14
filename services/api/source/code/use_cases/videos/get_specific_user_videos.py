from typing import List, Union, Callable
from uuid import UUID
from models import Video, SortKeys
from data_access.rds.abstract import VideosDB
from use_cases.validation_utils import is_same_user

# get specific user videos
def make_get_specific_user_videos(videos: VideosDB) -> Callable[[Union[UUID, str], UUID], List[Video]]:
    async def get_specific_user_videos(authenticated_user_id: Union[UUID, str], user_id: UUID) -> List[Video]:
        # build visibility settings by matching selected user id to the viewer
        if is_same_user(authenticated_user_id, user_id):
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
