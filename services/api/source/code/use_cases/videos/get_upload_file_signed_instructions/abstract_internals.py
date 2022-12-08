from uuid import UUID
from typing import Protocol
from external_systems.data_access.rds.abstract.videos import VideosDatabase


class AssertFileContentTypeFunction(Protocol):
    def __call__(self, file_content_type: str) -> None:
        ...


class GenerateNewVideoHashIdFunction(Protocol):
    async def __call__(self, database: VideosDatabase, user_id: UUID) -> UUID:
        ...
