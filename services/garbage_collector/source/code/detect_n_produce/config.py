from shared.models.garbage.enums import GarbageTypes
from .models import ScanToTaskStepConfig
from functools import partial
# concrete imports
from shared.rds.videos import VideosDatabase
from shared.rds.unprocessed_videos import UnprocessedVideosDatabase
from common.constants import (
    VIDEOS_SCAN_LIMIT
)

producer_steps = [
    # Video marked for delete garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.VIDEO_DELETE.value,
        detect_garbage_fn=partial(
            VideosDatabase().get_marked_for_delete,
            limit=VIDEOS_SCAN_LIMIT
        )
    ),
    # Unprocessed video marked for delete garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.UNPROCESSED_VIDEO_DELETE.value,
        detect_garbage_fn=partial(
            UnprocessedVideosDatabase().get_marked_for_delete,
            limit=VIDEOS_SCAN_LIMIT
        )
    ),
    # Unprocessed video internal server error garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR.value,
        detect_garbage_fn=partial(
            UnprocessedVideosDatabase().get_failed_to_process,
            limit=VIDEOS_SCAN_LIMIT
        )
    ),
    # ...
    # User garbage
    # TBD
]
