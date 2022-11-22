from environment.environment import (
    SUPPORTED_VIDEO_TYPES,
    MAX_VIDEO_FILE_SIZE_IN_BYTES
)
from typing import Callable
from entities.storage import VideoUploadConfigRecord


# gets configurations to help users know video upload limitations
def make_get_video_upload_config() -> Callable[[], VideoUploadConfigRecord]:
    async def get_video_upload_config() -> VideoUploadConfigRecord:
        return VideoUploadConfigRecord(
            valid_file_types=list(SUPPORTED_VIDEO_TYPES),
            max_size_in_bytes=MAX_VIDEO_FILE_SIZE_IN_BYTES
        )

    return get_video_upload_config
