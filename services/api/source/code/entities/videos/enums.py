from enum import Enum

class VideoStages(str, Enum):
    """Stages a video can exist at"""

    UNPROCESSED = 'UNPROCESSED'
    READY = 'READY'
