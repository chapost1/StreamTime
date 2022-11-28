from environment import environment, constants
from typing import Awaitable, Callable
from fastapi import FastAPI, Request, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from external_systems.http_network_interface.routers import list as routers
import common.app_errors as app_errors

app = FastAPI()

origins = [
    environment.UI_HOST_URL,
    'http://localhost:4200', # temp
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

startup_task: Awaitable = lambda: ...
shutdown_task: Awaitable = lambda: ...

def register_startup_task(do: Awaitable) -> None:
    global startup_task
    startup_task = do

def register_shutdown_task(do: Awaitable) -> None:
    global shutdown_task
    shutdown_task = do

@app.on_event('startup')
async def startup_event():
    await startup_task()

@app.on_event('shutdown')
async def shutdown_event():
    await shutdown_task()

def http_error(details: app_errors.AppError, status_code: status) -> Response:
    if details is not None:
        return JSONResponse(content=details, status_code=status_code)
    else:
        return Response(content=details, status_code=status_code)

@app.middleware('http')
async def app_errors_handler(request: Request, call_next: Callable):
    try:
        return await call_next(request)
    except app_errors.NotFoundError as e:
        return http_error(details=e.details, status_code=status.HTTP_404_NOT_FOUND)
    except app_errors.InputError as e:
        return http_error(details=e.details, status_code=status.HTTP_400_BAD_REQUEST)
    except app_errors.UnauthorizedError as e:
        return http_error(details=e.details, status_code=status.HTTP_401_UNAUTHORIZED)
    except app_errors.AccessDeniedError as e:
        return http_error(details=e.details, status_code=status.HTTP_403_FORBIDDEN)
    except app_errors.TooEarlyError as e:
        return http_error(details=e.details, status_code=status.HTTP_425_TOO_EARLY)


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