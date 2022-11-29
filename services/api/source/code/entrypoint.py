import common.environment as environment
from external_systems.http_network_interface import HttpServer
from app_lifecycle_hooks import (
    on_startup,
    on_shutdown
)


def run() -> None:
    server = HttpServer(
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        origins_whitelist=[
            environment.UI_HOST_URL,
            'http://localhost:4200', # temp
        ]
    )
    server.listen(
        port=environment.APP_PORT
    )


if __name__ == '__main__':
    run()
