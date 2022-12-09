from typing import Union, Optional
from uuid import UUID
from entities.videos import VideosPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from use_cases.videos.explore_listed_videos.helpers.abstract import (
    GetVisibilitySettingsFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    get_visibility_settings_fn: GetVisibilitySettingsFunction,
    # usage scope
    authenticated_user_id: Union[UUID, str],
    next: str,
    include_my: Optional[bool] = False
) -> VideosPage:
    """Gets Listed Videos"""

    user_id_to_ignore, authenticated_user_to_allow_privates = get_visibility_settings_fn(
        authenticated_user_id=authenticated_user_id,
        include_my=include_my
    )

    videos, next_page = await database.get_videos(
        ignore_user_id=user_id_to_ignore,
        include_privates_of_user_id=authenticated_user_to_allow_privates,
        filter_unlisted=True,
        next=next,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    return VideosPage(
        videos=videos,
        next=next_page
    )
