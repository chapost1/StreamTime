from typing import Protocol
from entities.storage import FileUploadSignedInstructions

class Storage(Protocol):
    """Storage client class protocol"""

    async def get_upload_file_signed_instructions(self, item_relative_path: str, file_content_type: str) -> FileUploadSignedInstructions:
        """
        returns valid upload file signed instuctions
        """


    async def get_file_signed_url(self, item_relative_path: str, signature_duration_seconds: int) -> str:
        """
        returns a signed url to view a resource for certain time
        """


    async def delete_file(self, item_relative_path: str) -> None:
        """
        deletes a file
        """
