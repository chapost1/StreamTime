from uuid import UUID
from typing import Union
from use_cases.validation_utils.abstract import IsSameUserFn


def is_access_allowed(
    # creation scope
    is_same_user_fn: IsSameUserFn,
    # usage scope
    authenticated_user_id: Union[UUID, str],
    owner_user_id: UUID,
    is_private: bool
) -> bool:
    is_same_user = is_same_user_fn(
        id_a=authenticated_user_id, id_b=owner_user_id
    )
    if is_same_user:
        return True

    return not is_private
