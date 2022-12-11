from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import Union
from uuid import UUID
from entities.videos import VideosPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase


async def use_case(
    # creation scope
    database: VideosDatabase,
    # usage scope
    authenticated_user_id: Union[UUID, str],
    user_id: UUID,
    next: str
) -> VideosPage:
    """
    Gets Specific User Listed Videos
    i.e: when some user want to see another user videos in particular
            one should not be able to see unlisted videos of others
            and if it is the same user, this call is intended to help the user know
            how it's own 'page' looks for another users.
            otherwise, he can use get_authenticated_user call instead
    """

    # TODO: validate if target user actually exists

    videos, next_page = await database.get_videos(
        user_id=user_id,
        include_privates_of_user_id=authenticated_user_id,
        filter_unlisted=True,
        next=next,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    return VideosPage(
        videos=videos,
        next=next_page
    )
