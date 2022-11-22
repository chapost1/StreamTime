from dataclasses import dataclass
from typing import Optional

@dataclass
class Context:
    bucket: str
    upload_prefix: str
    region: Optional[str] = None
