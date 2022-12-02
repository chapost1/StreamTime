from typing import List, Union, Callable, Optional, Tuple
from uuid import UUID
from entities.videos import Video
from use_cases.validation_utils import is_anonymous_user
from external_systems.data_access.rds.abstract import VideosDB


def get_explore_visibility_settings(authenticated_user_id: Union[UUID, str], include_my: Optional[bool]) -> Tuple[UUID, UUID]:
    is_authenticated_user = not is_anonymous_user(authenticated_user_id)

    allow_privates_of_user_id = None
    exclude_user_id = None

    if is_authenticated_user:
        # let the authenticated user to view it's own private videos if he will
        allow_privates_of_user_id = authenticated_user_id

        if not include_my:
            # user wants to excldue its own videos while exploring
            exclude_user_id = authenticated_user_id
    
    return exclude_user_id, allow_privates_of_user_id


def make_explore_listed_videos(videos: VideosDB) -> Callable[[Union[UUID, str], Optional[bool]], List[Video]]:
    async def explore_listed_videos(authenticated_user_id: Union[UUID, str], include_my: Optional[bool] = False) -> List[Video]:
        
        exclude_user_id, allow_privates_of_user_id = get_explore_visibility_settings(
            authenticated_user_id=authenticated_user_id,
            include_my=include_my
        )

        return await videos.get_listed_videos(
            allow_privates_of_user_id=allow_privates_of_user_id,
            exclude_user_id=exclude_user_id
        )

    return explore_listed_videos
