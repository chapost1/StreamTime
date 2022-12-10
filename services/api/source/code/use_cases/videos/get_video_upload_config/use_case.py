from entities.storage import VideoUploadConfigRecord
from common.environment import (
    SUPPORTED_VIDEO_TYPES,
    MAX_VIDEO_FILE_SIZE_IN_BYTES
)


async def use_case() -> VideoUploadConfigRecord:
    """
    Gets Video upload config

    The purpose of the configurations is to help users know video upload limitations
    """

    return VideoUploadConfigRecord(
        valid_file_types=list(SUPPORTED_VIDEO_TYPES),
        max_size_in_bytes=MAX_VIDEO_FILE_SIZE_IN_BYTES
    )
