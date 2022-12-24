from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime


class UploadedVideo(BaseModel):
    hash_id: Optional[UUID]
    user_id: Optional[UUID]
    file_name: Optional[str]
    upload_time: Optional[datetime.datetime]
