from models.videos.uploaded_video import UploadedVideo
from typing import Optional

class UnprocessedVideo(UploadedVideo):
    failure_reason: Optional[str]

    def is_still_processing(self) -> bool:
        return self.failure_reason is None
    
    def is_failed(self) -> bool:
        return self.failure_reason is not None
