from typing import Union, Protocol, Tuple
from uuid import UUID


class GetVisibilitySettingsFunction(Protocol):
    def __call__(self, authenticated_user_id: Union[UUID, str], include_my: bool) -> Tuple[UUID, UUID]:
        ...
