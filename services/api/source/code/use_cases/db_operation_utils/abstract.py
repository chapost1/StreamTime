from typing import List, Dict, Any, Protocol
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable,
    Updatable,
    Deletable
)


class SearchDbFn(Protocol):
    async def __call__(self, searchable: Searchable) -> List[Any]:
        ...


class UpdateDbFn(Protocol):
    async def __call__(self, updatable: Updatable, new_desired_state: Dict) -> None:
        ...


class DeleteDbFn(Protocol):
    async def __call__(self, deletable: Deletable) -> None:
        ...
