from entities.videos import Video
from common.utils import calc_server_time
from uuid import uuid4
from mock import patch
from use_cases.videos.update_video.helpers.listed_videos_preparations import (
    prepare_listed_record_before_update
)


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id'})
def test_not_changing_input():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    snapshot = input.dict()
    prepare_listed_record_before_update(video=input)
    assert input.dict() == snapshot


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id'})
def test_returns_input_without_not_allowed_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    result = prepare_listed_record_before_update(video=input)
    assert result.upload_time is None
    assert result.user_id is not None
    assert result.hash_id is not None


@patch('entities.videos.Video.ALLOWED_UPDATE_FIELDS_FOR_LISTED_VIDEOS', {'user_id', 'hash_id', 'upload_time'})
def test_returns_input_with_all_allowed_fields():
    input: Video = Video(
        user_id=uuid4(),
        hash_id=uuid4(),
        upload_time=calc_server_time()
    )
    result = prepare_listed_record_before_update(video=input)
    assert result == input