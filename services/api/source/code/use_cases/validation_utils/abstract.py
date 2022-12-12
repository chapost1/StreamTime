from typing import Dict, List, Union, Protocol
from uuid import UUID


class AssertRequiredFieldFunction(Protocol):
    def __call__(self, entity: Dict, fields: List[str]) -> None:
        """
        Validates Entity holds the intended fields as properties
        If not, raises an excepiton
        """

class FailOnUnsupportedFieldsFunction(Protocol):
    def __call__(self, entity: Dict, supported_fields: List[str]) -> None:
        """
        Validates Entity has only supported fields
        If it anything else, raises an excepiton

        Agenda: for example, user sends unsupported fields for update
        """


class IsSameUserFunction(Protocol):
    def __call__(self, id_a: Union[UUID, str], id_b: Union[UUID, str]) -> bool:
        """Compares a pair of users ids"""


class IsAnonymouseUserFunction(Protocol):
    def __call__(self, user_id: Union[UUID, str]) -> bool:
        """Checks if a user id is actually a mark for anonymous user"""
