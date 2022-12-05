from entities.storage.video_upload_config_record import VideoUploadConfigRecord
import pytest
from pydantic import ValidationError


def test_should_require_max_size_in_bytes_argument():
    with pytest.raises(expected_exception=ValidationError):
        VideoUploadConfigRecord(valid_file_types=[])


def test_should_require_valid_file_types_argument():
    with pytest.raises(expected_exception=ValidationError):
        VideoUploadConfigRecord(max_size_in_bytes=123)


def test_should_not_fail_on_valid_arguments():
    VideoUploadConfigRecord(max_size_in_bytes=123, valid_file_types=[])
    assert 1 == 1
