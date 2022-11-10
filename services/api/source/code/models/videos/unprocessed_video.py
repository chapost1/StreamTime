from models.videos.uploaded_video import UploadedVideo
from typing import Optional

class UnprocessedVideo(UploadedVideo):
    failure_reason: Optional[str]
