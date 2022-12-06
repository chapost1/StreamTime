from entities.videos.video import Video
from common.utils import calc_server_time
import pytest
from pydantic import ValidationError
import random


def test_video_can_be_initialized_without_arguments():
    # the purpose of his test is that use may send a video for update with partial fields
    # and none of the fields are an exception as a must
    vid = Video()
    assert vid is not None


def test_private_key_storage_object_key_can_be_initialized():
    storage_object_key = 'some_value'
    vid = Video(storage_object_key=storage_object_key)
    assert vid.storage_object_key == storage_object_key


def test_private_key_storage_object_key_can_be_initialized():
    storage_thumbnail_key = 'some_value'
    vid = Video(storage_thumbnail_key=storage_thumbnail_key)
    assert vid.storage_thumbnail_key == storage_thumbnail_key


def test_is_listed_is_false_when_listing_time_is_null():
    vid = Video()
    assert vid.is_listed() == False
    assert vid.is_not_listed() == True


def test_is_listed_is_true_when_listing_time_is_a_valid_time():
    vid = Video(listing_time=calc_server_time())
    assert vid.is_listed() == True
    assert vid.is_not_listed() == False


def test_listing_time_wont_accept_invalid_datetime():
    with pytest.raises(expected_exception=ValidationError):
        Video(listing_time='not datetime')


def test_pagination_index_argument_existence():
    pagination_index = random.randint(0, 100)
    vid = Video(pagination_index=pagination_index)
    assert vid.pagination_index == pagination_index


def test_title_argument_existence():
    title = 'dummy title'
    vid = Video(title=title)
    assert vid.title == title


def test_description_argument_existence():
    description = 'some desc'
    vid = Video(description=description)
    assert vid.description == description


def test_video_type_argument_existence():
    video_type = 'video/mp4'
    vid = Video(video_type=video_type)
    assert vid.video_type == video_type


def test_size_in_bytes_argument_existence():
    size_in_bytes = random.randint(0, 100)
    vid = Video(size_in_bytes=size_in_bytes)
    assert vid.size_in_bytes == size_in_bytes


def test_description_argument_existence():
    duration_seconds = random.randint(0, 100)
    vid = Video(duration_seconds=duration_seconds)
    assert vid.duration_seconds == duration_seconds


def test_is_private_argument_existence():
    expected = True
    vid = Video(is_private=expected)
    assert vid.is_private == expected


def test_should_fail_with_invalid_url_as_thumbnail_url():
    with pytest.raises(expected_exception=ValidationError):
        Video(thumbnail_url='invalid')


def test_should_not_fail_using_real_url_as_thumbnail_url():
    # on the go it assert its existence
    some_valid_url = 'https://foo.bar.com'
    vid = Video(thumbnail_url=some_valid_url)
    assert vid.thumbnail_url == some_valid_url


def test_required_fields_property():
    assert Video.REQUIRED_FIELDS_ON_LISTING == ['title', 'description']


def test_allowed_update_fields_property():
    assert Video.ALLOWED_UPDATE_FIELDS == {'title', 'description', 'listing_time', 'is_private'}
