import common.environment as environment
from common.app_errors import InputError


def assert_file_content_type(file_content_type: str) -> None:
    if file_content_type not in environment.SUPPORTED_VIDEO_TYPES:
        raise InputError(f'unsupported video file type::{file_content_type}, try one of these: {environment.SUPPORTED_VIDEO_TYPES}')
