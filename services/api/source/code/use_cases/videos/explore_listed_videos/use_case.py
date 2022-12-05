from typing import Union, Optional, Protocol, List, Tuple
from uuid import UUID
from entities.videos import VideosPage, Video, NextPage
from entities.videos.abstract_protocols import (
    NextPageTextDecoder,
    NextVideosPageCalculator
)
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.videos import VideosDescriber
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)
from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT


class DescribeVideosFn(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        user_id_to_ignore: UUID,
        authenticated_user_to_allow_privates: UUID,
        pagination_index_is_smaller_than: int,
        page_limit: int
    ) -> Searchable:
        ...


class GetVisibilitySettingsFn(Protocol):
    def __call__(self, authenticated_user_id: Union[UUID, str], include_my: bool) -> Tuple[UUID, UUID]:
        ...


async def use_case(
    # creation scope
    database: VideosDatabase,
    describe_videos_fn: DescribeVideosFn,
    get_visibility_settings_fn: GetVisibilitySettingsFn,
    next_page_text_decoder: NextPageTextDecoder,
    next_videos_page_calculator: NextVideosPageCalculator,
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

    next_page: NextPage = next_page_text_decoder.decode(b64=next)

    videos_describer: VideosDescriber = describe_videos_fn(
        database=database,
        user_id_to_ignore=user_id_to_ignore,
        authenticated_user_to_allow_privates=authenticated_user_to_allow_privates,
        pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    videos: List[Video] = await videos_describer.search()

    return VideosPage(
        videos=videos,
        next=next_videos_page_calculator.calc_next_page(videos=videos)
    )
