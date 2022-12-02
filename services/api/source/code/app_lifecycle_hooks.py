from external_systems.data_access.rds.pg import init as init_rds, terminate as terminate_rds
from external_systems.aws_integration import init as init_boto3
import asyncio


async def on_startup() -> None:
    """Initialize services the app relies on"""

    initialization_tasks = [
        init_rds,
        init_boto3
    ]
    async with asyncio.TaskGroup() as tg:
        for init_target in initialization_tasks:
            tg.create_task(init_target())


async def on_shutdown() -> None:
    """Gracefully terminates services the app relies on"""

    await terminate_rds()
