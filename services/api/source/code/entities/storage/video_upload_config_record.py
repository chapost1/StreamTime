from dataclasses import dataclass
from typing import List


@dataclass
class VideoUploadConfigRecord:
    max_size_in_bytes: int
    valid_file_types: List[str]
