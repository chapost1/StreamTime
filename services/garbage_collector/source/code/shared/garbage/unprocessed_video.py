from __future__ import annotations
from typing import Protocol
from shared.garbage.uploaded_video import UploadedVideo
from shared.rds.abstract import Database
from dataclasses import dataclass


class UnprocessedVideosDatabase(Database, Protocol):
    def delete_garbage(self, video: UnprocessedVideo) -> None:
        ...


@dataclass
class UnprocessedVideo(UploadedVideo):
    database: UnprocessedVideosDatabase


    def delete(self) -> None:
        self.database.delete_garbage(
            user_id=self.user_id,
            hash_id=self.hash_id
        )


    def to_message(self) -> str:
        return super().to_message()
