from uuid import UUID
from typing import Union, Protocol


class IsAccessAllowedFunction(Protocol):
    def __call__(
        self,
        authenticated_user_id: Union[UUID, str],
        owner_user_id: UUID,
        is_private: bool
    ) -> bool:
        ...
