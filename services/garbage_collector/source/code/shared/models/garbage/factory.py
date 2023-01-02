from .enums import GarbageTypes
from .garbage import Garbage
from .unprocessed_video import UnprocessedVideo
from .video import Video


video_types = {
    GarbageTypes.VIDEO_DELETE.value
}
unprocessed_video_types = {
    GarbageTypes.UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR.value,
    GarbageTypes.UNPROCESSED_VIDEO_DELETE.value
}


class GarbageFactory:
    """Factory for garbage objects"""

    @staticmethod
    def create(type: GarbageTypes, **kwargs) -> Garbage:
        """Creates a garbage object based on the type."""

        if type in video_types:
            return Video(
                type=type,
                **kwargs
            )
        elif type in unprocessed_video_types:
            return UnprocessedVideo(
                type=type,
                **kwargs
            )
        else:
            raise Exception(f"Unsupported garbage type: {type}")
