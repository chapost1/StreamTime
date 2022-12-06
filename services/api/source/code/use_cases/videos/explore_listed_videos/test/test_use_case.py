from typing import List, Any
from use_cases.videos.explore_listed_videos.use_case import use_case
from entities.videos import VideosPage, Video, NextPage
from uuid import uuid4
from use_cases.videos.explore_listed_videos.get_visibility_settings import get_visibility_settings
from use_cases.db_operation_utils.concrete import search_db
import pytest
from functools import partial
from use_cases.validation_utils.concrete import is_anonymous_user

# as all the internal used functions, are tested
# this test purpose is just check everything is 'stitched' together

@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mocks
    class NextPageTextDecoder:
        def decode(self, b64: str) -> NextPage:
            return NextPage()

    videos = [
        Video(user_id=uuid4(), hash_id=uuid4()),
        Video(user_id=uuid4(), hash_id=uuid4())
    ]

    mock_calculated_page_next = str(uuid4())

    class Searchable:
        async def search(self) -> List[Any]:
            return videos

    class DescribeDbVideosFn:
        def __call__(self, *args, **kwds) -> Searchable:
            return Searchable()
    
    class NextVideosPageCalculator:
        def calc_next_page(self, videos: List[Video]) -> str:
            return mock_calculated_page_next

    # execute
    result = await use_case(
        database=None,
        search_db_fn=search_db,
        get_visibility_settings_fn=partial(get_visibility_settings, is_anonymous_user_fn=is_anonymous_user),
        next_page_text_decoder=NextPageTextDecoder(),
        describe_db_videos_fn=DescribeDbVideosFn(),
        next_videos_page_calculator=NextVideosPageCalculator(),
        authenticated_user_id=uuid4(),
        next=None,
        include_my=False
    )

    assert result == VideosPage(
        videos=videos,
        next=mock_calculated_page_next
    )
