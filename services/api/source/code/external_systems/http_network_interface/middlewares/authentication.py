from environment import constants
from typing import Callable
from fastapi import Request

async def inject_temporary_dummy_username(request: Request, call_next: Callable):
    # dummy values
    is_user_authentication_verified = True
    authenticated_user_id = 'ae6d14eb-d222-4967-98d9-60a7cc2d7891'

    if is_user_authentication_verified:
        request.state.auth_user_id = authenticated_user_id
    else:
        request.state.auth_user_id = constants.ANONYMOUS_USER

    return await call_next(request)

async def authenticate_user(*args, **kwargs):
    return await inject_temporary_dummy_username(*args, **kwargs)