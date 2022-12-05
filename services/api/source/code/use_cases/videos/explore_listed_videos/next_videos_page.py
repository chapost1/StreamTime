from typing import List, Protocol
from uuid import UUID
from entities.videos import Video, VideosPage, NextPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase


class SearchVideosFn(Protocol):
    async def __call__(
        self,
        database: VideosDatabase,
        pagination_index_is_smaller_than: int,
        user_id_to_ignore: UUID,
        authenticated_user_to_allow_privates: UUID
    ) -> List[Video]:
        ...


async def next_videos_page(
    database: VideosDatabase,
    search_videos_fn: SearchVideosFn,
    next: str,
    user_id_to_ignore: UUID,
    authenticated_user_to_allow_privates: UUID
) -> VideosPage:
    next_page = NextPage.decode(next)

    videos: List[Video] = await search_videos_fn(
        database=database,
        user_id_to_ignore=user_id_to_ignore,
        authenticated_user_to_allow_privates=authenticated_user_to_allow_privates,
        pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than
    )

    return VideosPage(
        videos=videos,
        next=VideosPage.calc_next_page(videos=videos)
    )