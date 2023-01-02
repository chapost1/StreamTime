from __future__ import annotations
from typing import Optional, Protocol
from shared.models.garbage.uploaded_video import UploadedVideo
from shared.rds.abstract import Database
import json
from dataclasses import dataclass


class VideosDatabase(Database, Protocol):
    def delete_garbage(self, video: Video) -> None:
        ...


@dataclass
class Video(UploadedVideo):
    thumbnail_url: Optional[str] = None
    storage_object_key: Optional[str] = None
    storage_thumbnail_key: Optional[str] = None


    def delete(self, database: VideosDatabase) -> None:
        try:
            database.begin()

            database.delete_garbage(
                video=self
            )

            # TODO: delete from storage

            database.commit()
        except Exception:
            database.rollback()
            raise
    

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
