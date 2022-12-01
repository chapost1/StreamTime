from typing import List
from starlette.applications import Starlette
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from external_systems.http_network_interface.middlewares.errorhandling import app_errors_handler
from external_systems.http_network_interface.middlewares.authentication import authenticate_user

def attach_middlewares(
    app: Starlette,
    origins_whitelist: List[str] = ("*")
) -> None:
    # notice: order does matter, if we put cors before error handlers, the raise error will occur before the cors headers are added to response
    app.add_middleware(BaseHTTPMiddleware, dispatch=app_errors_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_whitelist,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=authenticate_user)
