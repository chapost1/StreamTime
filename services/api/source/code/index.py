import uvicorn
from external_systems.http_network_interface import (
    app,
    register_startup_task,
    register_shutdown_task
)
from app_lifecycle_hooks import (
    on_startup,
    on_shutdown
)

register_startup_task(on_startup)
register_shutdown_task(on_shutdown)

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=80, workers=1)
