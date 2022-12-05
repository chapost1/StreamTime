from typing import Union, Tuple
from uuid import UUID
from use_cases.validation_utils.abstract import IsAnonymouseUserFn


def get_visibility_settings(
    # creation scope
    is_anonymous_user_fn: IsAnonymouseUserFn,
    # usage scope
    authenticated_user_id: Union[UUID, str],
    include_my: bool,
) -> Tuple[bool, bool]:

    # if user wants to excldue its own videos while exploring, then mark it as excluded
    user_id_to_ignore = None
    if not include_my:
        user_id_to_ignore = authenticated_user_id

    # allow authenticated user to view it's own private videos
    authenticated_user_to_allow_privates = None
    if not is_anonymous_user_fn(user_id=authenticated_user_id):
        authenticated_user_to_allow_privates = authenticated_user_id    

    return user_id_to_ignore, authenticated_user_to_allow_privates
