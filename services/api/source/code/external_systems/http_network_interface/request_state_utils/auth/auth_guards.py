from environment import constants
from fastapi import Request, HTTPException, status
from external_systems.http_network_interface.request_state_utils.auth import auth_state
from uuid import UUID
from typing import Union


async def authenticated_user(request: Request) -> UUID:
    authenticated_user_id: Union[UUID, str] = await any_user(request=request)
    if str(authenticated_user_id) == constants.ANONYMOUS_USER:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return authenticated_user_id


async def any_user(request: Request) -> Union[UUID, str]:
    try:
        authenticated_user_id: UUID = auth_state.get_authenticated_user_id(request=request)
        return authenticated_user_id
    except KeyError:
        return constants.ANONYMOUS_USER
