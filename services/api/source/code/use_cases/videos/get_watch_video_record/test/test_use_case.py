from entities.videos import WatchVideoRecord, Video
from common.constants import MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
from common.app_errors import AccessDeniedError
from use_cases.db_operation_utils.concrete import search_one_in_database
from external_systems.data_access.storage.storage_test_client import StorageTestClient
from typing import List, Any
from uuid import uuid4
import pytest
from use_cases.videos.get_watch_video_record.helpers import is_access_allowed
from use_cases.videos.get_watch_video_record import use_case

user_id = uuid4()
hash_id = uuid4()

storage_object_key = f'{user_id}/{hash_id}'

mock_host = 'https://mock.com'

storage = StorageTestClient(host=mock_host)


def get_db_describer_to_return_vidoe_on_search(video: Video):
    class Searchable:
        async def search(self) -> List[Any]:
            return [video]

    return lambda *args, **kwds: Searchable()


@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    # mock
    video: Video = Video(
        user_id=user_id,
        hash_id=hash_id,
        storage_object_key=storage_object_key
    )

    # execute
    result = await use_case(
        # creation scope
        database=None,
        storage=storage,
        search_one_in_database_fn=search_one_in_database,
        describe_videos_in_database_fn=get_db_describer_to_return_vidoe_on_search(video=video),
        is_access_allowed_fn=is_access_allowed,
        # usage scope
        authenticated_user_id=user_id,
        user_id=user_id,
        hash_id=hash_id
    )

    expected_watchable_url = await storage.get_file_signed_url(
        item_relative_path=storage_object_key,
        signature_duration_seconds=MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
    )

    assert result == WatchVideoRecord(
        video=video,
        watchable_url=expected_watchable_url
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

    # execute
    try:
        await use_case(
            # creation scope
            database=None,
            storage=storage,
            search_one_in_database_fn=search_one_in_database,
            describe_videos_in_database_fn=get_db_describer_to_return_vidoe_on_search(video=video),
            is_access_allowed_fn=is_access_allowed,
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