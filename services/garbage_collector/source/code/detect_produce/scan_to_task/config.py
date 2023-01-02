from shared.models.garbage.enums import GarbageTypes
from .models import ScanToTaskStepConfig
# concrete imports
from shared.rds.videos import VideosDatabase
from shared.rds.unprocessed_videos import UnprocessedVideosDatabase
from common.constants import (
    VIDEOS_SCAN_LIMIT
)

producer_steps = [
    # Video garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.VIDEO_DELETE.value,
        get_database=VideosDatabase,
        scan_limit=VIDEOS_SCAN_LIMIT
    ),
    # Unprocessed video garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.UNPROCESSED_VIDEO_DELETE.value,
        get_database=UnprocessedVideosDatabase,
        scan_limit=VIDEOS_SCAN_LIMIT
    )
    # TODO: add unprocessed_video_internal_server_error garbage flow
    # ...
    # User garbage
    # TBD
]
