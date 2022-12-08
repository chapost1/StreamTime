from typing import List, Dict, Any, Protocol
from external_systems.data_access.rds.abstract.common_protocols import (
    Searchable,
    Updatable,
    Deletable
)


class SearchInDatabaseFunction(Protocol):
    """Searches for all records which matches the searchable"""
    async def __call__(self, searchable: Searchable) -> List[Any]:
        ...

class SearchOneInDatabaseFunction(Protocol):
    """Searches for one record and raise not found exception if not found"""
    async def __call__(searchable: Searchable) -> Any:
        ...

class UpdateInDatabaseFunction(Protocol):
    """Updates the described records with the new state key arguments"""
    async def __call__(self, updatable: Updatable, new_desired_state: Dict) -> None:
        ...


class DeleteInDatabaseFunction(Protocol):
    """Deletes the described records"""
    async def __call__(self, deletable: Deletable) -> None:
        ...
