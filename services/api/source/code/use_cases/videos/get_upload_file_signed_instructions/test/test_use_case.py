from use_cases.videos.get_upload_file_signed_instructions.use_case import use_case
from entities.storage import FileUploadSignedInstructions
from uuid import uuid4
from external_systems.data_access.storage.storage_test_client import StorageTestClient
import pytest
from common.app_errors import InputError
from asyncmock import AsyncMock

user_id = uuid4()
hash_id = uuid4()

object_key = f'{user_id}/{hash_id}'

mock_host = 'https://mock.com'

storage = StorageTestClient(host=mock_host)

MP4 = 'mp4'

@pytest.mark.asyncio
async def test_returns_expected_structure_with_returned_values_in_internals():
    result = await use_case(
        database=None,
        storage=storage,
        assert_file_content_type_fn=lambda file_content_type: ...,
        generate_new_video_hash_id_fn=AsyncMock(return_value=hash_id),
        authenticated_user_id=user_id,
        file_content_type=MP4
    )

    assert result == FileUploadSignedInstructions(
        url=f'{mock_host}/{object_key}',
        signatures={
            'file_content_type': MP4
        }
    )


@pytest.mark.asyncio
async def test_propragate_exception_of_assert_file_content_type_fn():
    def raise_input_error(file_content_type: str) -> None:
        raise InputError()
    try:
        await use_case(
            database=None,
            storage=storage,
            assert_file_content_type_fn=raise_input_error,
            generate_new_video_hash_id_fn=AsyncMock(return_value=hash_id),
            authenticated_user_id=user_id,
            file_content_type=MP4
        )
        # should not reach here
        assert 1 == 2
    except InputError:
        # good, desired exception has been thrown
        assert 1 == 1
