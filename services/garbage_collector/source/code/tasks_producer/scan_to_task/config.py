from shared.garbage.enums import GarbageTypes
from functools import partial
from shared.garbage.factory import GarbageFactory
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
        garbage_type=GarbageTypes.VIDEO.value,
        get_database=partial(VideosDatabase, garbage_factory=GarbageFactory),
        scan_limit=VIDEOS_SCAN_LIMIT
    ),
    # Unprocessed video garbage
    ScanToTaskStepConfig(
        garbage_type=GarbageTypes.UNPROCESSED_VIDEO.value,
        get_database=partial(UnprocessedVideosDatabase, garbage_factory=GarbageFactory),
        scan_limit=VIDEOS_SCAN_LIMIT
    )
    # ...
    # User garbage
    # TBD
]
