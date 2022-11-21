from dataclasses import dataclass
from typing import Dict
from pydantic import HttpUrl

@dataclass
class FileUploadSignedInstructions:
    url: HttpUrl
    signatures: Dict
