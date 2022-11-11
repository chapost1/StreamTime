from typing import Protocol
from models.storage import FileUploadUrlRecord

class Storage(Protocol):
    async def get_upload_file_url(self, item_key: str) -> FileUploadUrlRecord:
        """
        returns valid upload file url and required fields for validation
        """
