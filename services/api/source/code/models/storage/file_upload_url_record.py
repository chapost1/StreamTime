from pydantic import BaseModel
from typing import Dict
from pydantic import HttpUrl


class FileUploadUrlRecord(BaseModel):
    url: HttpUrl
    fields: Dict
