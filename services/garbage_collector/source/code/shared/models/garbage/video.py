from __future__ import annotations
from typing import Optional, Protocol, Any
from shared.models.garbage.uploaded_video import UploadedVideo
from shared.infrastructure.rds.abstract import Database
from shared.infrastructure.storage.abstract import StorageClient
import asyncio
import json
from dataclasses import dataclass


class VideosDatabase(Database, Protocol):
    async def delete(self, video: Video, connection: Optional[Any]) -> None:
        ...


@dataclass
class Video(UploadedVideo):
    thumbnail_url: Optional[str] = None
    storage_object_key: Optional[str] = None
    storage_thumbnail_key: Optional[str] = None


    async def delete(self, database: VideosDatabase, storage: StorageClient) -> None:
        async with database.transaction as connection:
            # everything under the same transaction

            # delete video assets from storage
            storage_delete_tasks = [
                storage.delete_file(
                    item_relative_path=self.storage_object_key
                ),
                storage.delete_file(
                    item_relative_path=self.storage_thumbnail_key
                )
            ]
            # perform database and storage deletions in parallel
            tasks = [
                asyncio.gather(*storage_delete_tasks),
                database.delete(
                    video=self,
                    connection=connection
                )
            ]

            await asyncio.gather(*tasks)


    def to_message(self) -> str:
        return json.dumps(
            {
                'type': self.type,
                'user_id': str(self.user_id),
                'hash_id': str(self.hash_id),
                'thumbnail_url': self.thumbnail_url,
                'storage_object_key': self.storage_object_key,
                'storage_thumbnail_key': self.storage_thumbnail_key
            }
        )
