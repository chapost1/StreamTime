from typing import List, Union, Callable
from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.abstract import VideosDB
from use_cases.videos.utils import get_cross_users_visibility_settings


def make_get_specific_user_videos(database: VideosDB) -> Callable[[Union[UUID, str], UUID], List[Video]]:
    """Creates Get Specific User Videos use case"""

    async def get_specific_user_videos(authenticated_user_id: Union[UUID, str], user_id: UUID) -> List[Video]:
        """Gets Specific User Videos"""

        # TODO: validate if target user actually exists

        visibility_settings = get_cross_users_visibility_settings(
            authenticated_user_id=authenticated_user_id,
            user_id=user_id
        )

        return await database.get_user_videos(
            user_id=user_id,
            hide_private=visibility_settings.hide_private,
            hide_unlisted=visibility_settings.hide_unlisted,
            sort_key=visibility_settings.sort_key
        )

    return get_specific_user_videos
