from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List, Union, Callable
from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.abstract.videos import VideosDB


def make_get_specific_user_listed_videos(database: VideosDB) -> Callable[[Union[UUID, str], UUID], List[Video]]:
    """Creates Get Specific User Listed Videos use case"""

    async def get_specific_user_listed_videos(
        authenticated_user_id: Union[UUID, str],
        user_id: UUID,
        pagination_index_is_smaller_than: int
    ) -> List[Video]:
        """
        Gets Specific User Listed Videos
        i.e: when some user want to see another user videos in particular
             one should not be able to see unlisted videos of others
             and if it is the same user, this call is intended to help the user know
             how it's own 'page' looks for another users.
             otherwise, he can use get_authenticated_user call instead
        """

        # TODO: validate if target user actually exists

        return await (
            database.get_videos_explorer()
            .of_user(user_id=user_id)
            .hide_unlisted(flag=True)
            .allow_privates_of(user_id=authenticated_user_id)
            .paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
            .limit(limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT)
            .search()
        )

    return get_specific_user_listed_videos
