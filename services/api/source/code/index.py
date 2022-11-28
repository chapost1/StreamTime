import uvicorn
from environment import environment
from external_systems.http_network_interface import (
    app,
    register_startup_task,
    register_shutdown_task
)
from app_lifecycle_hooks import (
    on_startup,
    on_shutdown
)

if __name__ == '__main__':
    register_startup_task(on_startup)
    register_shutdown_task(on_shutdown)
    uvicorn.run(app=app, host='0.0.0.0', port=environment.APP_PORT, workers=1)
