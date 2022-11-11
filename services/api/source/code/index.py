from environment import environment, constants
from typing import Callable
from fastapi import FastAPI, Request
from routers import list as routers
from app_startup import init as init_services

app = FastAPI()

@app.on_event('startup')
async def init():
    await init_services()

@app.middleware('http')# todo: replace with actual authentication mechanism
async def inject_temporary_dummy_username(request: Request, call_next: Callable):
    # dummy values
    is_user_authentication_verified = True
    authenticated_user_id = 'ae6d14eb-d222-4967-98d9-60a7cc2d7891'

    if is_user_authentication_verified:
        request.state.auth_user_id = authenticated_user_id
    else:
        request.state.auth_user_id = constants.ANONYMOUS_USER

    return await call_next(request)

@app.get(environment.HEALTH_CHECK_PATH)
async def health_check():
    return {'message': 'ok'}

app.include_router(routers.videos_router, prefix='/video')
