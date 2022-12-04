from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List, Union, Callable, Optional
from uuid import UUID
from entities.videos import Video, VideosPage, NextPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from use_cases.validation_utils import is_anonymous_user


def make_explore_listed_videos(database: VideosDatabase) -> Callable[[Union[UUID, str], Optional[bool]], VideosPage]:
    """Creates Explore Listed Videos use case"""

    async def explore_listed_videos(
        authenticated_user_id: Union[UUID, str],
        next: str,
        include_my: Optional[bool] = False
    ) -> VideosPage:
        """Gets Listed Videos"""

        # if user wants to excldue its own videos while exploring, then mark it as excluded
        user_id_to_ignore = None if include_my else authenticated_user_id
        # allow authenticated user to view it's own private videos
        authenticated_user_to_allow_privates = None if is_anonymous_user(user_id=authenticated_user_id) else authenticated_user_id

        next_page = NextPage.decode(next)

        videos: List[Video] = await (
            database.describe_videos()
            .not_owned_by(user_id=user_id_to_ignore)
            .include_privates_of(user_id=authenticated_user_to_allow_privates)
            .filter_unlisted(flag=True)
            .paginate(pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than)
            .limit(limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT)
            .search()
        )

        return VideosPage(
            videos=videos,
            next=VideosPage.calc_next_page(videos=videos)
        )

    return explore_listed_videos
