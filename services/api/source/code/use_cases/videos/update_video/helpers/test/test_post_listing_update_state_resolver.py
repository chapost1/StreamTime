from entities.videos import Video
from common.utils import calc_server_time
from uuid import uuid4
from mock import patch
from common.app_errors import InputError
import pytest
from use_cases.videos.update_video.helpers.post_listing_update_state_resolver import (
    resolve_update_state
)


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id'})
def test_fails_on_unsupported_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        # V unsupported V
        upload_time=calc_server_time()
    )
    with pytest.raises(expected_exception=InputError):
        resolve_update_state(video=input)


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id', 'upload_time'})
def test_not_fails_on_supported_fields_only():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    resolve_update_state(video=input)
    assert 1 == 1


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id', 'upload_time'})
def test_not_fails_returns_dict_with_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    result = resolve_update_state(video=input)
    expected_result = {
        'user_id': input.user_id,
        'hash_id': input.hash_id,
        'upload_time': input.upload_time
    }
    assert result == expected_result


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id', 'upload_time'})
def test_not_fails_returns_dict_without_none_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=None,
        upload_time=calc_server_time()
    )
    result = resolve_update_state(video=input)
    expected_result = {
        'user_id': input.user_id,
        'upload_time': input.upload_time
    }
    assert result == expected_result


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id', 'upload_time'})
def test_not_fails_not_affecting_input():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    snapshot = input.copy()
    resolve_update_state(video=input)

    assert input == snapshot
