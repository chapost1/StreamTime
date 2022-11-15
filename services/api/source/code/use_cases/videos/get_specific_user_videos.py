from typing import List, Union, Callable
from uuid import UUID
from models import Video
from data_access.rds.abstract import VideosDB
from use_cases.videos.utils import get_cross_users_visibility_settings

# get specific user videos
def make_get_specific_user_videos(videos: VideosDB) -> Callable[[Union[UUID, str], UUID], List[Video]]:
    async def get_specific_user_videos(authenticated_user_id: Union[UUID, str], user_id: UUID) -> List[Video]:
        hide_private, hide_unlisted, sort_key = get_cross_users_visibility_settings(
            authenticated_user_id=authenticated_user_id,
            user_id=user_id
        )

        return await videos.get_user_videos(
            user_id=user_id,
            hide_private=hide_private,
            hide_unlisted=hide_unlisted,
            sort_key=sort_key
        )

    return get_specific_user_videos
