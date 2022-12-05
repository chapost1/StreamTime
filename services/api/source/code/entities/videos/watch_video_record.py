from pydantic import BaseModel, HttpUrl
from entities.videos.video import Video


class WatchVideoRecord(BaseModel):
    watchable_url: HttpUrl
    video: Video
