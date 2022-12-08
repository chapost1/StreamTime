from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from typing import List, Union
from uuid import UUID
from entities.videos import Video, VideosPage, NextPage
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)
from entities.videos.abstract_protocols import (
    NextPageTextDecoder,
    NextVideosPageCalculator
)
from use_cases.db_operation_utils.abstract import SearchInDatabaseFunction
from use_cases.videos.get_specific_user_listed_videos.abstract_internals import (
    DescribeVideosInDatabaseFunction
)


async def use_case(
    # creation scope
    database: VideosDatabase,
    search_in_database_fn: SearchInDatabaseFunction,
    describe_videos_in_database_fn: DescribeVideosInDatabaseFunction,
    next_page_text_decoder: NextPageTextDecoder,
    next_videos_page_calculator: NextVideosPageCalculator,
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

    next_page: NextPage = next_page_text_decoder.decode(b64=next)

    db_videos_describer: Searchable = describe_videos_in_database_fn(
        database=database,
        authenticated_user_id=authenticated_user_id,
        user_id=user_id,
        pagination_index_is_smaller_than=next_page.pagination_index_is_smaller_than,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    videos: List[Video] = await search_in_database_fn(searchable=db_videos_describer)

    return VideosPage(
        videos=videos,
        next=next_videos_page_calculator.calc_next_page(videos=videos)
    )
