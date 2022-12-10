from use_cases.videos.get_authenticated_user_videos.use_case import use_case
from entities.videos import Video, UnprocessedVideo, UserVideosList
from uuid import uuid4
import pytest
from unittest.mock import (
    AsyncMock
)


@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mocks

    videos = [
        Video(user_id=uuid4(), hash_id=uuid4()),
        Video(user_id=uuid4(), hash_id=uuid4())
    ]

    unprocessed_videos = [
        UnprocessedVideo(user_id=uuid4(), hash_id=uuid4())
    ]

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        videos,
        None
    )
    mock_database.get_unprocessed_videos.return_value = unprocessed_videos
    
    call_authenticated_user_id = uuid4()

    # execute
    result = await use_case(
        database=mock_database,
        # usage scope
        authenticated_user_id=call_authenticated_user_id
    )

    assert result == UserVideosList(
        unprocessed_videos=unprocessed_videos,
        videos=videos
    )

    # assert that the mock objects were called with the expected arguments
    mock_database.get_unprocessed_videos.assert_any_call(
        include_user_id=call_authenticated_user_id,
    )
    mock_database.get_videos.assert_any_call(
        include_user_id=call_authenticated_user_id,
        # always
        filter_unlisted=False,
        include_privates_of_user_id=call_authenticated_user_id
    )
