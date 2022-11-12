from pydantic import BaseModel
from typing import Dict
from pydantic import HttpUrl


class FileUploadSignedInstructions(BaseModel):
    url: HttpUrl
    signatures: Dict
