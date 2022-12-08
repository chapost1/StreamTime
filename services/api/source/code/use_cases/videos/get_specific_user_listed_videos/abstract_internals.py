from typing import Protocol
from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)


class DescribeVideosInDatabaseFunction(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        authenticated_user_id: UUID,
        user_id: UUID,
        pagination_index_is_smaller_than: int,
        page_limit: int
    ) -> Searchable:
        ...
