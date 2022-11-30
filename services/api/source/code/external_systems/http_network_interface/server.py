import uvicorn
from typing import Awaitable, List
from external_systems.http_network_interface.asgi_app import create_new_asgi_app
from external_systems.http_network_interface.middlewares import attach_middlewares
from external_systems.http_network_interface.routers import attach_routers


class HttpServer:
    __slots__ = (
        'app'
    )

    def __init__(
        self,
        origins_whitelist: List[str] = ("*"),
        on_startup: Awaitable = lambda: ...,
        on_shutdown: Awaitable = lambda: ...,
    ):
        self.app = create_new_asgi_app(
            origins_whitelist=origins_whitelist,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            attach_middlewares_fn=attach_middlewares,
            attach_routers_fn=attach_routers
        )

    def listen(
        self,
        port: int
    ) -> None:
        uvicorn.run(app=self.app, host='0.0.0.0', port=port, workers=1)