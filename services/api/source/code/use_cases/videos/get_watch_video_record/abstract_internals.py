from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from typing import Union, Protocol
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)


class DescribeDbVideosFn(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        authenticated_user_id: UUID,
        user_id: UUID,
        hash_id: UUID
    ) -> Searchable:
        ...


class IsAccessAllowedFn(Protocol):
    def __call__(
        self,
        authenticated_user_id: Union[UUID, str],
        owner_user_id: UUID,
        is_private: bool
    ) -> bool:
        ...
