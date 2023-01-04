

class StorageClient:
    """Abstract class for storage clients."""

    async def delete_file(self, item_relative_path: str) -> None:
        """Delete a file from the storage service."""
