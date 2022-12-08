from typing import List, Any
from use_cases.videos.get_authenticated_user_videos.use_case import use_case
from entities.videos import Video, UnprocessedVideo, UserVideosList
from uuid import uuid4
from use_cases.db_operation_utils.concrete import search_in_database
import pytest


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

    class SearchableVideos:
        async def search(self) -> List[Any]:
            return videos
    
    class SearchableUnprocessedVideos:
        async def search(self) -> List[Any]:
            return unprocessed_videos

    # execute
    result = await use_case(
        database=None,
        search_in_database_fn=search_in_database,
        describe_unprocessed_videos_in_database_fn=lambda *args, **kwds: SearchableUnprocessedVideos(),
        describe_videos_in_database_fn=lambda *args, **kwds: SearchableVideos(),
        # usage scope
        authenticated_user_id=uuid4()
    )

    assert result == UserVideosList(
        unprocessed_videos=unprocessed_videos,
        videos=videos
    )
