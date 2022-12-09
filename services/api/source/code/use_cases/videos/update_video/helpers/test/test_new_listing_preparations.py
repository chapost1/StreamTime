from common.app_errors import InputError
from entities.videos import Video
from common.utils import calc_server_time
from uuid import uuid4
import pytest
from mock import patch
from use_cases.videos.update_video.helpers.new_listing_preparations import (
    prepare_new_listing_before_publish
)


def new_video() -> Video:
    return Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', [])
def test_not_changing_input():
    input: Video = new_video()
    snapshot = input.dict()
    prepare_new_listing_before_publish(video=input)
    assert input.dict() == snapshot


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', [])
def test_returns_input_with_listing_time():
    input: Video = new_video()
    result = prepare_new_listing_before_publish(video=input)
    assert input.listing_time is None
    assert result.listing_time is not None
    input.listing_time = result.listing_time
    assert result == input


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['title'])
def test_raise_InputError_if_missing_required_fields():
    with pytest.raises(expected_exception=InputError):
        input: Video = new_video()
        if input.title is not None:
            input.title = None
        prepare_new_listing_before_publish(video=input)


@patch('entities.videos.Video.REQUIRED_FIELDS_ON_LISTING', ['title'])
def test_not_raising_error_if_required_fields_are_not_missing():
    input: Video = new_video()
    if input.title is None:
        input.title = uuid4()
    prepare_new_listing_before_publish(video=input)
