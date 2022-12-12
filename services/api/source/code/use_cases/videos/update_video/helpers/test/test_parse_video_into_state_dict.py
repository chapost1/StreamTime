from entities.videos import Video
from uuid import uuid4
from use_cases.videos.update_video.helpers.parse_video_into_state_dict import (
    parse_video_into_state_dict
)


def test_return_value_includes_only_allowed_update_fields_nothing():
    input = Video(user_id=uuid4())
    assert parse_video_into_state_dict(video=input, include_fields=[]) == {}


def test_return_value_includes_only_allowed_update_fields_not_empty():
    input = Video(user_id=uuid4(), is_private=True)
    assert parse_video_into_state_dict(video=input, include_fields=['user_id', 'is_private']) == {
        'is_private': input.is_private,
        'user_id': input.user_id
    }


def test_omit_none_values():
    input = Video(user_id=None, is_private=True)
    assert parse_video_into_state_dict(video=input, include_fields=['user_id', 'is_private']) == {
        'is_private': input.is_private,
    }
