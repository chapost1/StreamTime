from __future__ import annotations
from typing import Protocol
from shared.models.garbage.uploaded_video import UploadedVideo
from dataclasses import dataclass


class UnprocessedVideosDatabase(Protocol):
    def delete_garbage(self, video: UnprocessedVideo) -> None:
        ...
    
    def mark_as_internal_server_error(self, video: UnprocessedVideo) -> None:
        ...


@dataclass
class UnprocessedVideo(UploadedVideo):

    def delete(self, database: UnprocessedVideosDatabase) -> None:
        database.delete_garbage(
            video=self
        )
    

    def mark_as_internal_server_error(self, database: UnprocessedVideosDatabase) -> None:
        database.mark_as_internal_server_error(
            video=self
        )


    def to_message(self) -> str:
        return super().to_message()
