from entities.storage import FileUploadSignedInstructions
from pydantic import HttpUrl


default_host = 'https://mock.com'


class StorageTestClient:
    """Storage client class for testing"""
    host: HttpUrl

    def __init__(self, host: HttpUrl = default_host) -> None:
        self.host = host

    async def get_upload_file_signed_instructions(self, item_relative_path: str, file_content_type: str) -> FileUploadSignedInstructions:
        return FileUploadSignedInstructions(
            url=f'{self.host}/{item_relative_path}',
            signatures={
                'file_content_type': file_content_type
            }
        )


    async def get_file_signed_url(self, item_relative_path: str, signature_duration_seconds: int) -> str:
        return f'{self.host}/{item_relative_path}?signature_duration_seconds={signature_duration_seconds}'


    async def delete_file(self, item_relative_path: str) -> None:
        return None
