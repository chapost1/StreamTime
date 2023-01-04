from __future__ import annotations
from typing import Protocol
from shared.models.garbage.uploaded_video import UploadedVideo
from shared.rds.abstract import Database
from dataclasses import dataclass


class UnprocessedVideosDatabase(Database, Protocol):
    async def delete(self, video: UnprocessedVideo) -> None:
        ...
    
    async def mark_as_internal_server_error(self, video: UnprocessedVideo) -> None:
        ...


@dataclass
class UnprocessedVideo(UploadedVideo):

    async def delete(self, database: UnprocessedVideosDatabase) -> None:
        await database.delete(
            video=self
        )


    async def mark_as_internal_server_error(self, database: UnprocessedVideosDatabase) -> None:
        async with database.transaction() as connection:
            # everythin in the same transaction
            await database.mark_as_internal_server_error(
                    video=self,
                    connection=connection
            )

            # TODO: send SNS to notify the user
        


    def to_message(self) -> str:
        return super().to_message()
