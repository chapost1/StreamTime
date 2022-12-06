from fastapi import Request
from typing import Union
from uuid import UUID
from external_systems.http_network_interface.request_state_utils.auth.abstract_internals import HasState


"""
The purpose of this file is \
to abstract the logic of accessing an authenticated user id state \
inside the request object
"""


def set_authenticated_user_id(request: HasState, authenticated_user_id: Union[UUID, str]) -> None:
    request.state.auth_user_id = authenticated_user_id


def get_authenticated_user_id(request: HasState) -> Union[str, None]:
    return request.state.auth_user_id
