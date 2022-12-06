from use_cases.videos.get_video_upload_config.use_case import use_case
from entities.storage.video_upload_config_record import VideoUploadConfigRecord
from common.environment import SUPPORTED_VIDEO_TYPES, MAX_VIDEO_FILE_SIZE_IN_BYTES


async def test_sturcture():
    # almost identical to the usecase itself, and might be not much a required test
    # this only purpose of this test is to make sure nothing is broke
    assert await use_case == VideoUploadConfigRecord(
        valid_file_types=list(SUPPORTED_VIDEO_TYPES),
        max_size_in_bytes=MAX_VIDEO_FILE_SIZE_IN_BYTES
    )