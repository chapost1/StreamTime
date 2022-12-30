from __future__ import annotations
from typing import Optional, Protocol
from shared.garbage.uploaded_video import UploadedVideo
from shared.rds.abstract import Database
import json
from dataclasses import dataclass


class VideosDatabase(Database, Protocol):
    def delete_garbage(self, video: Video) -> None:
        ...


@dataclass
class Video(UploadedVideo):
    database: VideosDatabase

    thumbnail_url: Optional[str] = None
    storage_object_key: Optional[str] = None
    storage_thumbnail_key: Optional[str] = None


    def delete(self) -> None:
        try:
            self.database.begin()

            self.database.delete_garbage(
                user_id=self.user_id,
                hash_id=self.hash_id
            )

            # TODO: delete from storage

            self.database.commit()
        except Exception:
            self.database.rollback()
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
