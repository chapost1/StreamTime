from functools import partial
from shared.models.garbage.enums import GarbageTypes
from shared.models.garbage.garbage import Garbage
from shared.models.bag.bag import GarbageBag

from shared.models.garbage.video import Video
from shared.models.garbage.unprocessed_video import UnprocessedVideo

# fixme to use abstraction for db injection
from shared.rds.videos import VideosDatabase
from shared.rds.unprocessed_videos import UnprocessedVideosDatabase


class Bagger:
    """Creates garbage bags based on the garbage type."""

    @staticmethod
    def bag(garbage: Garbage) -> GarbageBag:
        """Creates a garbage object based on the type."""

        type = garbage.type

        if type == GarbageTypes.VIDEO_DELETE.value:
            garbage: Video = garbage
            return GarbageBag(
                collect_fn=partial(
                    garbage.delete,
                    database=VideosDatabase()
                )
            )
        elif type == GarbageTypes.UNPROCESSED_VIDEO_INTERNAL_SERVER_ERROR.value:
            garbage: UnprocessedVideo = garbage
            return GarbageBag(
                collect_fn=partial(
                    garbage.mark_as_internal_server_error,
                    database=UnprocessedVideosDatabase()
                )
            )
        elif type == GarbageTypes.UNPROCESSED_VIDEO_DELETE.value:
            garbage: UnprocessedVideo = garbage
            return GarbageBag(
                collect_fn=partial(
                    garbage.delete,
                    database=UnprocessedVideosDatabase()
                )
            )
        else:
            raise Exception(f"Unsupported garbage type: {type}")
