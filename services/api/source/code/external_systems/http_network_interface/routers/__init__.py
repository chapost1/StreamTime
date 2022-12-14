from fastapi import FastAPI
from external_systems.http_network_interface.routers import list as routers

def attach_routers(app: FastAPI) -> None:
    """Accepts FastAPI app and attaches application routers to it"""

    app.include_router(routers.root_router, prefix='')

    app.include_router(routers.videos_router, prefix='/video')
