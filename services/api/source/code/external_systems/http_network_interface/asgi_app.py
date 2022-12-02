from starlette.applications import Starlette
from typing import Awaitable, Protocol, List
from fastapi import FastAPI


class AttachMiddlewaresFn(Protocol):
    def __call__(self, app: Starlette, origins_whitelist: List[str]) -> None: ...


class AttachRoutersFn(Protocol):
    def __call__(self, app: Starlette) -> None: ...


def create_new_asgi_app(
    origins_whitelist: List[str],
    on_startup: Awaitable,
    on_shutdown: Awaitable,
    attach_middlewares_fn: AttachMiddlewaresFn,
    attach_routers_fn: AttachRoutersFn
) -> Starlette:
    """
    Creates an ASGI app
    Attaches essentials as middlewares, routers and up/down events to it on creation
    """

    asgi_app = FastAPI(
        on_startup=[on_startup],
        on_shutdown=[on_shutdown]
    )

    attach_middlewares_fn(
        app=asgi_app,
        origins_whitelist=origins_whitelist
    )

    attach_routers_fn(
        app=asgi_app
    )

    return asgi_app
