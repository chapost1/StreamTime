from pydantic import BaseModel
from typing import List


class VideoUploadConfigRecord(BaseModel):
    max_size_in_bytes: int
    valid_file_types: List[str]
