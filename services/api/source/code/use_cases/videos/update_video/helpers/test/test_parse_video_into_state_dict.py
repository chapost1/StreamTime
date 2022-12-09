from entities.videos import Video
from uuid import uuid4
from mock import patch
from use_cases.videos.update_video.helpers.parse_video_into_state_dict import (
    parse_video_into_state_dict
)


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {})
def test_return_value_includes_only_allowed_update_fields_nothing():
    input = Video(user_id=uuid4())
    assert parse_video_into_state_dict(video=input) == {}


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'is_private'})
def test_return_value_includes_only_allowed_update_fields_not_empty():
    input = Video(user_id=uuid4(), is_private=True)
    assert parse_video_into_state_dict(video=input) == {
        'is_private': input.is_private,
        'user_id': input.user_id
    }


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_NEW_LISTING', {'user_id', 'is_private'})
def test_omit_none_values():
    input = Video(user_id=None, is_private=True)
    assert parse_video_into_state_dict(video=input) == {
        'is_private': input.is_private,
    }
