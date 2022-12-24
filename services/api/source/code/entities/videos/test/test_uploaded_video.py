from entities.videos.uploaded_video import UploadedVideo
from pydantic import ValidationError
from uuid import uuid4
import pytest
from common.utils import calc_server_time
import datetime

def test_uploaded_video_can_be_initialized_without_arguments():
    vid = UploadedVideo()
    assert vid is not None


def test_uploaded_video_hash_id_required_uuid():
    with pytest.raises(expected_exception=ValidationError):
        UploadedVideo(hash_id='not uuid')


def test_uploaded_video_user_id_required_uuid():
    with pytest.raises(expected_exception=ValidationError):
        UploadedVideo(user_id='not uuid')


def test_uploaded_video_file_name_required_str():
    with pytest.raises(expected_exception=ValidationError):
        # unparsable string
        UploadedVideo(file_name={})


def test_uploaded_video_upload_time_requires_valid_datetime():
    with pytest.raises(expected_exception=ValidationError):
        UploadedVideo(upload_time='not datetime')


def test_uploaded_video_core_param_hash_id():
    hash_id = uuid4()
    vid = UploadedVideo(hash_id=hash_id)
    assert vid.hash_id == hash_id


def test_uploaded_video_core_param_user_id():
    user_id = uuid4()
    vid = UploadedVideo(user_id=user_id)
    assert vid.user_id == user_id


def test_uploaded_video_core_param_file_name():
    file_name = 'file name.mp4'
    vid = UploadedVideo(file_name=file_name)
    assert vid.file_name == file_name


def test_uploaded_video_core_param_upload_time():
    upload_time = calc_server_time()
    vid = UploadedVideo(upload_time=upload_time)
    iso_formatted = vid.upload_time.replace(tzinfo=datetime.timezone.utc).isoformat()
    assert iso_formatted == upload_time
