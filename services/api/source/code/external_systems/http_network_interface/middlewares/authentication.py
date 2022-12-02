import common.constants as constants
from typing import Callable
from fastapi import Request
from external_systems.http_network_interface.request_state_utils.auth import auth_state

def verify_is_user_authenticated(request: Request) -> bool:
    # dummy logic
    is_user_authentication_verified = True
    return is_user_authentication_verified


def detect_authenticated_user_id(request: Request) -> str:
    authenticated_user_id = constants.ANONYMOUS_USER

    if verify_is_user_authenticated(request=request):
        # dummy value
        authenticated_user_id = 'ae6d14eb-d222-4967-98d9-60a7cc2d7891'

    return authenticated_user_id

def inject_authenticated_user_id(request: Request) -> None:
    authenticated_user_id = detect_authenticated_user_id(request=request)
    auth_state.set_authenticated_user_id(
        request=request,
        authenticated_user_id=authenticated_user_id
    )

async def authenticate_user(request: Request, call_next: Callable):
    """Authenticates user"""
    # TODO: implement actual authentication logic

    inject_authenticated_user_id(request=request)

    return await call_next(request)
