from pydantic import BaseModel
from uuid import UUID
from typing import Optional
import datetime

class Video(BaseModel):
    hash_id: UUID
    user_id: UUID
    title: str
    description: str
    size_in_bytes: int
    duration_seconds: int
    video_type: str
    thumbnail_url: str
    upload_time: datetime.datetime
    is_private: Optional[bool]
    is_listed: Optional[bool]
