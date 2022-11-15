from typing import List, Union, Callable, Optional
from uuid import UUID
from models import Video
from use_cases.validation_utils import is_anonymous_user
from data_access.rds.abstract import VideosDB

def make_explore_listed_videos(videos: VideosDB) -> Callable[[Union[UUID, str], Optional[bool]], List[Video]]:
    async def explore_listed_videos(authenticated_user_id: Union[UUID, str], include_my: Optional[bool] = False) -> List[Video]:
        is_authenticated_user = not is_anonymous_user(authenticated_user_id)

        if is_authenticated_user:
            # let the authenticated user to view it's own private videos if he will
            # it won't appear unless user wants to see it's own videos anyway
            allow_privates_of_user_id = authenticated_user_id

            if include_my:# user wants to see its own videos while exploring
                exclude_user_id = None
            else:# user wants to excldue its videos
                exclude_user_id = authenticated_user_id

        return await videos.get_listed_videos(
            allow_privates_of_user_id=allow_privates_of_user_id,
            exclude_user_id=exclude_user_id
        )

    return explore_listed_videos
