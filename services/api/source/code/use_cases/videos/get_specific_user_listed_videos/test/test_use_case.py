from typing import List, Any
from use_cases.videos.get_specific_user_listed_videos.use_case import use_case
from entities.videos import Video, VideosPage, NextPage
from uuid import uuid4
from use_cases.db_operation_utils.concrete import search_db
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
        # creation scope
        database=None,
        search_db_fn=search_db,
        describe_db_videos_fn=lambda *args, **kwargs: Searchable(),
        next_page_text_decoder=NextPageTextDecoder(),
        next_videos_page_calculator=NextVideosPageCalculator(),
        # usage scope
        authenticated_user_id=uuid4(),
        user_id=uuid4(),
        next=None
    )

    assert result == VideosPage(
        videos=videos,
        next=mock_calculated_page_next
    )
