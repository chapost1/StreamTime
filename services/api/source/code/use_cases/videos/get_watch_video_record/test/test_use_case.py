from entities.videos import WatchVideoRecord, Video
from common.constants import MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
from common.app_errors import AccessDeniedError
from external_systems.data_access.storage.storage_test_client import StorageTestClient
from uuid import uuid4
import pytest
from use_cases.videos.get_watch_video_record.helpers import is_access_allowed
from use_cases.videos.get_watch_video_record import use_case
from unittest.mock import (
    Mock,
    AsyncMock
)


auth_user_id = uuid4()
user_id = uuid4()
hash_id = uuid4()

storage_object_key = f'{user_id}/{hash_id}'

mock_host = 'https://mock.com'


@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mock
    video: Video = Video(
        user_id=user_id,
        hash_id=hash_id,
        storage_object_key=storage_object_key,
        is_private=False
    )

    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        [video],
        None
    )
    
    spy_is_access_allowed = Mock(
        wraps=is_access_allowed
    )

    storage = StorageTestClient(host=mock_host)
    spy_storage = AsyncMock(wraps=storage)

    # execute
    result = await use_case(
        # creation scope
        database=mock_database,
        storage=spy_storage,
        is_access_allowed_fn=spy_is_access_allowed,
        # usage scope
        authenticated_user_id=user_id,
        user_id=user_id,
        hash_id=hash_id
    )

    # assert storage has been called as expected
    spy_storage.get_file_signed_url.assert_called_once_with(
        item_relative_path=storage_object_key,
        signature_duration_seconds=MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
    )

    # get from storage the expected result to compare
    expected_watchable_url = await storage.get_file_signed_url(
        item_relative_path=storage_object_key,
        signature_duration_seconds=MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
    )

    # compare
    assert result == WatchVideoRecord(
        video=video,
        watchable_url=expected_watchable_url
    )

    # assert that the mock objects were called with the expected arguments
    mock_database.get_videos.assert_any_call(
        user_id=user_id,
        hash_id=hash_id,
        # always
        filter_unlisted=True,
        include_privates_of_user_id=user_id
    )

    spy_is_access_allowed.assert_called_with(
        authenticated_user_id=user_id,
        owner_user_id=user_id,
        is_private=video.is_private
    )



@pytest.mark.asyncio
async def test_raise_access_denied_if_not_same_user_and_private():
    # mock
    video: Video = Video(
        user_id=user_id,
        hash_id=hash_id,
        storage_object_key=storage_object_key,
        is_private=True
    )


    mock_database = AsyncMock()
    mock_database.get_videos.return_value = (
        [video],
        None
    )
    
    spy_is_access_allowed = Mock(
        wraps=is_access_allowed
    )

    storage = StorageTestClient(host=mock_host)

    # execute
    try:
        await use_case(
            # creation scope
            database=mock_database,
            storage=storage,
            is_access_allowed_fn=spy_is_access_allowed,
            # usage scope
            authenticated_user_id=uuid4(),
            user_id=user_id,
            hash_id=hash_id
        )
        # should not succeed
        assert 1 == 2
    except AccessDeniedError:
        # as expected
        assert 1 == 1
