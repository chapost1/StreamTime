from uuid import UUID
from typing import Protocol
from external_systems.data_access.rds.abstract.videos import VideosDatabase


class AssertFileContentTypeFn(Protocol):
    def __call__(self, file_content_type: str) -> None:
        ...


class GenerateNewVideoHashIdFn(Protocol):
    async def __call__(self, database: VideosDatabase, user_id: UUID) -> UUID:
        ...
