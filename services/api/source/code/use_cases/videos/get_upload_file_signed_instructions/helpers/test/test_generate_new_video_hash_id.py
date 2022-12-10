from uuid import (
    UUID,
    uuid4
)
import pytest
from use_cases.videos.get_upload_file_signed_instructions.helpers.generate_new_video_hash_id import (
    generate_new_video_hash_id
)
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_raise_an_exception_if_find_video_stage_always_returns_value_not_none():
    # mocks
    mock_database = AsyncMock()
    mock_database.find_video_stage.return_value = uuid4()
    
    try:
        await generate_new_video_hash_id(database=mock_database, user_id=uuid4())
        # should not reach here
        assert 1 == 2
    except RuntimeError as e:
        # should raise exception
        assert 1 == 1


@pytest.mark.asyncio
async def test_return_some_valid_uuid_if_find_video_stage_returns_none():

    mock_database = AsyncMock()
    mock_database.find_video_stage.return_value = None

    hash_id = await generate_new_video_hash_id(database=mock_database, user_id=uuid4())
    try:
        # validate uuid4
        UUID(str(hash_id), version=4)
        # good
        assert 1 == 1
    except ValueError:
        # not a valid uuid
        assert 1 == 2
