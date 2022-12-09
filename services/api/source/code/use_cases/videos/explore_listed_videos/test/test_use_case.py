from typing import List, Any
from use_cases.videos.explore_listed_videos.use_case import use_case
from entities.videos import VideosPage, Video, NextPage
from uuid import uuid4
from use_cases.videos.explore_listed_videos.helpers import get_visibility_settings
from use_cases.db_operation_utils.concrete import search_in_database
import pytest


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
    
    class NextVideosPageCalculator:
        def calc_next_page(self, videos: List[Video]) -> str:
            return mock_calculated_page_next

    # execute
    result = await use_case(
        database=None,
        search_in_database_fn=search_in_database,
        get_visibility_settings_fn=get_visibility_settings,
        next_page_text_decoder=NextPageTextDecoder(),
        describe_videos_in_database_fn=lambda *args, **kwds: Searchable(),
        next_videos_page_calculator=NextVideosPageCalculator(),
        authenticated_user_id=uuid4(),
        next=None,
        include_my=False
    )

    assert result == VideosPage(
        videos=videos,
        next=mock_calculated_page_next
    )
