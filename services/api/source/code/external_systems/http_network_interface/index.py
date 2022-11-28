from fastapi import FastAPI
from typing import Awaitable
from environment import environment
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from external_systems.http_network_interface.routers import list as routers
from external_systems.http_network_interface.middlewares.errorhandling import app_errors_handler
from external_systems.http_network_interface.middlewares.authentication import authenticate_user

app = FastAPI()

def register_startup_task(do: Awaitable) -> None:
    app.add_event_handler('startup', do)

def register_shutdown_task(do: Awaitable) -> None:
    app.add_event_handler('shutdown', do)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        environment.UI_HOST_URL,
        'http://localhost:4200', # temp
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=app_errors_handler)
app.add_middleware(BaseHTTPMiddleware, dispatch=authenticate_user)

app.include_router(routers.root_router, prefix='')
app.include_router(routers.videos_router, prefix='/video')