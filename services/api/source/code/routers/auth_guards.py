from environment import constants
from fastapi import Request, HTTPException, status

async def authenticated_user(request: Request) -> str:
    authenticated_user_id: str = await any_user(request=request)
    if authenticated_user_id.__eq__(constants.ANONYMOUS_USER):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return authenticated_user_id

async def any_user(request: Request) -> str:
    try:
        authenticated_user_id: str = request.state.auth_user_id
        return authenticated_user_id
    except KeyError:
        return constants.ANONYMOUS_USER
