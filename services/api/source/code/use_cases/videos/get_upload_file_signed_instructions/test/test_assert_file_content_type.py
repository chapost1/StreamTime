from use_cases.videos.get_upload_file_signed_instructions.assert_file_content_type import assert_file_content_type
from common.app_errors import InputError
from mock import patch
import pytest


MP4 = 'mp4'
AVG = 'avg'

supported_video_types = {MP4, AVG}

@patch('common.environment.SUPPORTED_VIDEO_TYPES', supported_video_types)
def test_not_raising_an_exception_on_supported_video_type():
    assert assert_file_content_type(file_content_type=MP4) is None


def test__raising_an_exception_on_unsupported_video_type():
    # ofc uuid is not valid, no need to patch it
    with pytest.raises(expected_exception=InputError):
        assert_file_content_type(file_content_type=MP4)
