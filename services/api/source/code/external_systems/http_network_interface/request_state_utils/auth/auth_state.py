from fastapi import Request
from typing import Union
from uuid import UUID


"""
The purpose of this file is \
to abstract the logic of accessing an authenticated user id state \
inside the request object
"""


def set_authenticated_user_id(request: Request, authenticated_user_id: Union[UUID, str]) -> None:
    request.state.auth_user_id = authenticated_user_id


def get_authenticated_user_id(request: Request) -> Union[str, None]:
    return request.state.auth_user_id
