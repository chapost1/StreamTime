from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List, Union, Callable, Optional, Tuple
from uuid import UUID
from entities.videos import Video
from use_cases.validation_utils import is_anonymous_user
from external_systems.data_access.rds.abstract.videos import VideosDB


def get_explore_visibility_settings(authenticated_user_id: Union[UUID, str], include_my: bool) -> Tuple[UUID, UUID]:
    """
    Gets the visibility settings while exploring listed videos

    Args Explanation:
        include_my: A flag, used to select whether the selected user want to view it's own Videos
    
    Returns Explanation:
        exclude_user_id: The User id to hide it's videos, if any
        allow_privates_of_user_id: The User id to allow viewing it's own private assets, if any
    """

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


def make_explore_listed_videos(database: VideosDB) -> Callable[[Union[UUID, str], Optional[bool]], List[Video]]:
    """Creates Explore Listed Videos use case"""

    async def explore_listed_videos(
        authenticated_user_id: Union[UUID, str],
        pagination_index_is_smaller_than: int,
        include_my: Optional[bool] = False
    ) -> List[Video]:
        """Gets Listed Videos"""
        
        exclude_user_id, allow_privates_of_user_id = get_explore_visibility_settings(
            authenticated_user_id=authenticated_user_id,
            include_my=include_my
        )

        return await (
            database.get_videos_explorer()
            .allow_privates_of(user_id=allow_privates_of_user_id)
            .hide_unlisted(flag=True)
            .exclude_user(user_id=exclude_user_id)
            .paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
            .limit(limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT)
            .search()
        )

    return explore_listed_videos
