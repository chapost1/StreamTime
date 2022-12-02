from enum import Enum


class SortKeys(str, Enum):
    """Field to sort the videos list by it"""

    upload_time = 'upload_time'
    listing_time = 'listing_time'


class VideoStages(str, Enum):
    """Stages a video can exist at"""

    UNPROCESSED = 'UNPROCESSED'
    READY = 'READY'
