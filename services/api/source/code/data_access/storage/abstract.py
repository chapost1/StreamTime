from typing import Protocol
from models.storage import FileUploadSignedInstructions

class Storage(Protocol):
    async def get_upload_file_signed_instructions(self, item_key: str) -> FileUploadSignedInstructions:
        """
        returns valid upload file signed instuctions
        """
