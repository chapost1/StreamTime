from enum import Enum

class GarbageTypes(str, Enum):
    """The garbage types."""
    GARBAGE = "garbage"
    UPLOADED_VIDEO = "uploaded_video"
    VIDEO_DELETE = "video"
    UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR = "unprocessed_video_internal_server_error"
    UNPROCESSED_VIDEO_DELETE = "unprocessed_video"
