from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List, Union, Callable
from uuid import UUID
from entities.videos import Video, VideosPage, NextPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase


def make_get_specific_user_listed_videos(database: VideosDatabase) -> Callable[[Union[UUID, str], UUID], VideosPage]:
    """Creates Get Specific User Listed Videos use case"""

    async def get_specific_user_listed_videos(
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

        next_page = NextPage.decode(next)

        videos: List[Video] = await (
            database.describe_videos()
            .owned_by(user_id=user_id)
            .filter_unlisted(flag=True)
            .include_privates_of(user_id=authenticated_user_id)
            .paginate(pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than)
            .limit(limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT)
            .search()
        )

        return VideosPage(
            videos=videos,
            next=VideosPage.calc_next_page(videos=videos)
        )

    return get_specific_user_listed_videos
