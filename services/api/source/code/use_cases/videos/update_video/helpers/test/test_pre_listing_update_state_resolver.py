from common.app_errors import InputError
from entities.videos import Video
from common.utils import calc_server_time
from uuid import uuid4
import pytest
from mock import patch
from use_cases.videos.update_video.helpers.pre_listing_update_state_resolver import (
    resolve_update_state
)


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['listing_time'])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id'})
def test_raise_error_contains_unsupported_fields():
    input: Video = Video(
        user_id=uuid4()
    )
    resolve_update_state(video=input)
    assert 1 == 1


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['listing_time'])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id'})
def test_raise_error_contains_unsupported_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    with pytest.raises(expected_exception=InputError):
        resolve_update_state(video=input)


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['listing_time', 'user_id', 'upload_time'])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'hash_id', 'upload_time', 'listing_time'})
def test_not_fails_required_fields_are_ok():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time(),
        listing_time=calc_server_time()
    )
    result = resolve_update_state(video=input)
    assert result.get('listing_time', None) is not None
    expected_result = {
        'user_id': input.user_id,
        'hash_id': input.hash_id,
        'upload_time': input.upload_time,
        'listing_time': result.get('listing_time', None)
    }
    assert result == expected_result


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['listing_time'])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'hash_id', 'upload_time'})
def test_raise_error_missing_required_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    with pytest.raises(expected_exception=InputError):
        resolve_update_state(video=input)


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', [])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'hash_id', 'upload_time', 'listing_time'})
def test_not_fails_returns_dict_without_none_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=None,
        upload_time=calc_server_time()
    )
    result = resolve_update_state(video=input)
    assert result.get('listing_time', None) is not None
    expected_result = {
        'user_id': input.user_id,
        'listing_time': result.get('listing_time', None),
        'upload_time': input.upload_time
    }
    assert result == expected_result


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', [])
@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'hash_id', 'upload_time'})
def test_not_fails_not_affecting_input():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    snapshot = input.copy()
    resolve_update_state(video=input)

    assert input == snapshot
