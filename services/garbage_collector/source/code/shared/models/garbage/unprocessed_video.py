from __future__ import annotations
from typing import Protocol
from shared.models.garbage.uploaded_video import UploadedVideo
from shared.rds.abstract import Database
from dataclasses import dataclass


class UnprocessedVideosDatabase(Database, Protocol):
    def delete(self, video: UnprocessedVideo) -> None:
        ...
    
    def mark_as_internal_server_error(self, video: UnprocessedVideo) -> None:
        ...


@dataclass
class UnprocessedVideo(UploadedVideo):

    def delete(self, database: UnprocessedVideosDatabase) -> None:
        database.delete(
            video=self
        )


    def mark_as_internal_server_error(self, database: UnprocessedVideosDatabase) -> None:
        try:
            database.begin()

            database.mark_as_internal_server_error(
                video=self
            )

            # TODO: send SNS to notify the user

            database.commit()
        except Exception:
            database.rollback()
            raise


    def to_message(self) -> str:
        return super().to_message()
