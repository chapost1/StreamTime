from __future__ import annotations
from functools import partial
from .enums import GarbageTypes
from .garbage import Garbage
from .unprocessed_video import UnprocessedVideo
from .uploaded_video import UploadedVideo
from .video import Video

# fixme to use abstraction for db injection
from shared.rds.videos import VideosDatabase
from shared.rds.unprocessed_videos import UnprocessedVideosDatabase


class GarbageFactory:
    """Factory for garbage objects"""

    @staticmethod
    def create(type: GarbageTypes, **kwargs) -> Garbage:
        """Creates a garbage object based on the type."""

        if type == GarbageTypes.VIDEO.value:
            return Video(
                database=partial(VideosDatabase, garbage_factory=GarbageFactory),
                type=GarbageTypes.VIDEO.value,
                **kwargs
            )
        elif type == GarbageTypes.UNPROCESSED_VIDEO.value:
            return UnprocessedVideo(
                database=partial(UnprocessedVideosDatabase, garbage_factory=GarbageFactory),
                type=GarbageTypes.UNPROCESSED_VIDEO.value,
                **kwargs
            )
        elif type == GarbageTypes.UPLOADED_VIDEO.value:
            return UploadedVideo(
                type=GarbageTypes.UPLOADED_VIDEO.value,
                **kwargs
            )
        elif type == GarbageTypes.GARBAGE.value:
            return Garbage(
                type=GarbageTypes.GARBAGE.value,
                **kwargs
            )
        else:
            raise Exception(f"Unsupported garbage type: {type}")
