from dataclasses import dataclass
from pydantic import HttpUrl
from entities.videos.video import Video


@dataclass
class WatchVideoRecord:
    watchable_url: HttpUrl
    video: Video
