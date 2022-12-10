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



# chatGPT suggestion:
from unittest.mock import Mock
def test_use_case():
    # Set up the mock database and visibility settings function
    mock_database = Mock()
    mock_visibility_settings_fn = Mock()

    # Set up the expected return values for the mock objects
    mock_database.get_videos.return_value = ([
        {"id": 1, "name": "Video 1"},
        {"id": 2, "name": "Video 2"}],
        "next-page-token"
    )
    mock_visibility_settings_fn.return_value = (1, 2)

    # Call the use_case function with the mock objects
    result = use_case(
        database=mock_database,
        get_visibility_settings_fn=mock_visibility_settings_fn,
        authenticated_user_id="authenticated-user-id",
        next="next-page-token",
        include_my=True
    )

    # Assert that the use_case function returns the expected result
    assert result == VideosPage(
        videos=[
            {"id": 1, "name": "Video 1"},
            {"id": 2, "name": "Video 2"}
        ],
        next="next-page-token"
    )

    # Assert that the mock objects were called with the expected arguments
    mock_database.get_videos.assert_called_with(
        ignore_user_id=1,
        include_privates_of_user_id=2,
        filter_unlisted=True,
        next="next-page-token",
        page_limit=50
    )

    mock_visibility_settings_fn.assert_called_with(
        authenticated_user_id="authenticated-user-id",
        include_my=True
    )
