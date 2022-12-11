from use_cases.videos.explore_listed_videos.use_case import use_case
from entities.videos import VideosPage, Video
from uuid import uuid4
from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
import pytest
from unittest.mock import (
    Mock,
    AsyncMock
)
import random


@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mocks
    videos = [
        Video(user_id=uuid4(), hash_id=uuid4(), pagination_index=random.randint(1, 100)),
        Video(user_id=uuid4(), hash_id=uuid4(), pagination_index=random.randint(1, 100))
    ]

    next_page_token = VideosPage.calc_next_page(videos=videos)

    bools = [True, False]

    mock_visibility_settings_fn = Mock()
    not_user_id = random.choice(bools)
    include_privates_of_user_id = random.choice(bools)
    mock_visibility_settings_fn.return_value = (not_user_id, include_privates_of_user_id)

    call_authenticated_user_id = uuid4()
    call_next_page_token = uuid4()
    call_include_my = random.choice(bools)

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        videos,
        next_page_token
    )

    # execute
    result = await use_case(
        database=mock_database,
        get_visibility_settings_fn=mock_visibility_settings_fn,
        authenticated_user_id=call_authenticated_user_id,
        next=call_next_page_token,
        include_my=call_include_my
    )

    # assert that the use_case function returns the expected result
    assert result == VideosPage(
        videos=videos,
        next=next_page_token
    )

    # assert that the mock objects were called with the expected arguments
    mock_database.get_videos.assert_any_call(
        not_user_id=not_user_id,
        include_privates_of_user_id=include_privates_of_user_id,
        # always
        filter_unlisted=True,
        next=call_next_page_token,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )

    mock_visibility_settings_fn.assert_called_with(
        authenticated_user_id=call_authenticated_user_id,
        include_my=call_include_my
    )
