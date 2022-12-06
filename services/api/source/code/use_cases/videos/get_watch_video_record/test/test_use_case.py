from entities.videos import WatchVideoRecord, Video
from common.constants import MAXIMUM_SECONDS_TILL_PRESIGNED_URL_EXPIRATION
from common.app_errors import AccessDeniedError
from use_cases.db_operation_utils.concrete import search_one_db
from external_systems.data_access.storage.storage_test_client import StorageTestClient
from functools import partial
from typing import List, Any
from uuid import uuid4
import pytest
from use_cases.validation_utils.concrete import is_same_user
from use_cases.videos.get_watch_video_record.is_access_allowed import is_access_allowed
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

    class DescribeDbVideosFn:
        def __call__(self, *args, **kwds) -> Searchable:
            return Searchable()
    return DescribeDbVideosFn()


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
        search_one_db_fn=search_one_db,
        describe_db_videos_fn=get_db_describer_to_return_vidoe_on_search(video=video),
        is_access_allowed_fn=partial(is_access_allowed, is_same_user_fn=is_same_user),
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
    with pytest.raises(expected_exception=AccessDeniedError):
        await use_case(
            # creation scope
            database=None,
            storage=storage,
            search_one_db_fn=search_one_db,
            describe_db_videos_fn=get_db_describer_to_return_vidoe_on_search(video=video),
            is_access_allowed_fn=partial(is_access_allowed, is_same_user_fn=is_same_user),
            # usage scope
            authenticated_user_id=uuid4(),
            user_id=user_id,
            hash_id=hash_id
        )
