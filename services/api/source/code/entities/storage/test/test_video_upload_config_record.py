from entities.storage.video_upload_config_record import VideoUploadConfigRecord
import pytest
from pydantic import ValidationError
import random


def test_should_require_max_size_in_bytes_argument():
    with pytest.raises(expected_exception=ValidationError):
        VideoUploadConfigRecord(valid_file_types=[])


def test_should_require_valid_file_types_argument():
    with pytest.raises(expected_exception=ValidationError):
        VideoUploadConfigRecord(max_size_in_bytes=random.randint(0, 2e+9))


def test_should_fail_on_invalid_valid_file_types_not_str_parsable_list():
    with pytest.raises(expected_exception=ValidationError):
        VideoUploadConfigRecord(max_size_in_bytes=random.randint(0, 2e+9), valid_file_types=[{}])


def test_should_not_fail_on_valid_arguments():
    VideoUploadConfigRecord(max_size_in_bytes=random.randint(0, 2e+9), valid_file_types=[])
    assert 1 == 1
