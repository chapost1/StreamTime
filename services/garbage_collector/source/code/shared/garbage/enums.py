from enum import Enum

class GarbageTypes(str, Enum):
    """The garbage types."""
    GARBAGE = "garbage"
    UPLOADED_VIDEO = "uploaded_video"
    VIDEO = "video"
    UNPROCESSED_VIDEO = "unprocessed_video"
