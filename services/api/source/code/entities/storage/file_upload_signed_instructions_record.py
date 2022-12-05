from typing import Dict
from pydantic import BaseModel, HttpUrl


class FileUploadSignedInstructions(BaseModel):
    url: HttpUrl
    signatures: Dict
