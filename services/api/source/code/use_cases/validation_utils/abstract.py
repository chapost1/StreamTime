from typing import Any, List, Union, Protocol
from uuid import UUID


class AssertRequiredFieldFunction(Protocol):
    def __call__(self, entity: Any, fields: List[str]) -> None:
        """
        Validates Entity holds the intended fields as properties
        If not, raises an excepiton
        """


class IsSameUserFunction(Protocol):
    def __call__(self, id_a: Union[UUID, str], id_b: Union[UUID, str]) -> bool:
        """Compares a pair of users ids"""


class IsAnonymouseUserFunction(Protocol):
    def __call__(self, user_id: Union[UUID, str]) -> bool:
        """Checks if a user id is actually a mark for anonymous user"""
