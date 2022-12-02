from dataclasses import dataclass
from typing import Optional

@dataclass
class Context:
    """Context to conatain on what the S3 client should work on"""

    bucket: str
    upload_prefix: str
    region: Optional[str] = None
