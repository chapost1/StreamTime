from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List
from uuid import UUID
from entities.videos import Video
from external_systems.data_access.rds.abstract.videos import VideosDatabase


async def search_videos(
    database: VideosDatabase,
    user_id_to_ignore: UUID,
    authenticated_user_to_allow_privates: UUID,
    pagination_index_is_smaller_than: int
) -> List[Video]:
    return await (
        database.describe_videos()
        .not_owned_by(user_id=user_id_to_ignore)
        .include_privates_of(user_id=authenticated_user_to_allow_privates)
        .filter_unlisted(flag=True)
        .paginate(pagination_index_is_smaller_than=pagination_index_is_smaller_than)
        .limit(limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT)
        .search()
    )
