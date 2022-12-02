from common.environment import (
    SUPPORTED_VIDEO_TYPES,
    MAX_VIDEO_FILE_SIZE_IN_BYTES
)
from typing import Callable
from entities.storage import VideoUploadConfigRecord


def make_get_video_upload_config() -> Callable[[], VideoUploadConfigRecord]:
    """Creates Get Upload Video Config use case"""

    async def get_video_upload_config() -> VideoUploadConfigRecord:
        """
        Gets Video upload config

        The purpose of the configurations is to help users know video upload limitations
        """

        return VideoUploadConfigRecord(
            valid_file_types=list(SUPPORTED_VIDEO_TYPES),
            max_size_in_bytes=MAX_VIDEO_FILE_SIZE_IN_BYTES
        )

    return get_video_upload_config
