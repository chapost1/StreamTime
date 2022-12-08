from typing import Union, Protocol, Tuple
from uuid import UUID
from external_systems.data_access.rds.abstract.videos import VideosDatabase
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable
)


class DescribeVideosInDatabaseFunction(Protocol):
    def __call__(
        self,
        database: VideosDatabase,
        user_id_to_ignore: UUID,
        authenticated_user_to_allow_privates: UUID,
        pagination_index_is_smaller_than: int,
        page_limit: int
    ) -> Searchable:
        ...


class GetVisibilitySettingsFunction(Protocol):
    def __call__(self, authenticated_user_id: Union[UUID, str], include_my: bool) -> Tuple[UUID, UUID]:
        ...
