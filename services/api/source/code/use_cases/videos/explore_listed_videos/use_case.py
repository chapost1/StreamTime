from typing import Union, Optional, List
from uuid import UUID
from entities.videos import VideosPage, Video, NextPage
from entities.videos.abstract_protocols import (
    NextPageTextDecoder,
    NextVideosPageCalculator
)
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)
from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from use_cases.db_operation_utils.abstract import SearchInDatabaseFunction
from use_cases.videos.explore_listed_videos.abstract_internals import (
    DescribeVideosInDatabaseFunction,
    GetVisibilitySettingsFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_in_database_fn: SearchInDatabaseFunction,
    describe_videos_in_database_fn: DescribeVideosInDatabaseFunction,
    get_visibility_settings_fn: GetVisibilitySettingsFunction,
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

    db_videos_describer: Searchable = describe_videos_in_database_fn(
        database=database,
        user_id_to_ignore=user_id_to_ignore,
        authenticated_user_to_allow_privates=authenticated_user_to_allow_privates,
        pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    videos: List[Video] = await search_in_database_fn(searchable=db_videos_describer)

    return VideosPage(
        videos=videos,
        next=next_videos_page_calculator.calc_next_page(videos=videos)
    )
