from typing import Union, Optional, Protocol, List
from uuid import UUID
from entities.videos import VideosPage, Video
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.validation_utils import is_anonymous_user


class NextVideosPageFn(Protocol):
    async def __call__(
        self,
        database: VideosDatabase,
        next: str,
        user_id_to_ignore: UUID,
        authenticated_user_to_allow_privates: UUID
    ) -> List[Video]:
        ...


async def explore_listed_videos(
    database: VideosDatabase,
    next_videos_page_fn: NextVideosPageFn,
    authenticated_user_id: Union[UUID, str],
    next: str,
    include_my: Optional[bool] = False
) -> VideosPage:
    """Gets Listed Videos"""

    # if user wants to excldue its own videos while exploring, then mark it as excluded
    user_id_to_ignore = None if include_my else authenticated_user_id
    # allow authenticated user to view it's own private videos
    authenticated_user_to_allow_privates = None if is_anonymous_user(user_id=authenticated_user_id) else authenticated_user_id

    return await next_videos_page_fn(
        database=database,
        next=next,
        user_id_to_ignore=user_id_to_ignore,
        authenticated_user_to_allow_privates=authenticated_user_to_allow_privates
    )
