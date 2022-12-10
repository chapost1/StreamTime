from common.constants import LISTED_VIDEOS_QUERY_PAGE_LIMIT
from use_cases.videos.get_specific_user_listed_videos.use_case import use_case
from entities.videos import Video, VideosPage
from uuid import uuid4
import pytest
import random
from unittest.mock import (
    AsyncMock
)


@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mocks
    videos = [
        Video(user_id=uuid4(), hash_id=uuid4(), pagination_index=random.randint(1, 100)),
        Video(user_id=uuid4(), hash_id=uuid4(), pagination_index=random.randint(1, 100))
    ]

    next_page_token = VideosPage.calc_next_page(videos=videos)

    call_authenticated_user_id = uuid4()
    call_user_id = uuid4()
    call_next_page_token = uuid4()

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        videos,
        next_page_token
    )

    # execute
    result = await use_case(
        # creation scope
        database=mock_database,
        # usage scope
        authenticated_user_id=call_authenticated_user_id,
        user_id=call_user_id,
        next=call_next_page_token
    )

    assert result == VideosPage(
        videos=videos,
        next=next_page_token
    )

    # assert that the mock objects were called with the expected arguments
    mock_database.get_videos.assert_any_call(
        include_user_id=call_user_id,
        include_privates_of_user_id=call_authenticated_user_id,
        # always
        filter_unlisted=True,
        next=call_next_page_token,
        page_limit=LISTED_VIDEOS_QUERY_PAGE_LIMIT
    )
