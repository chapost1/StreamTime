from data_access.rds import init as init_rds
from aws import init as init_boto3
import asyncio

async def init():
    initialization_tasks = [
        init_rds,
        init_boto3
    ]
    async with asyncio.TaskGroup() as tg:
        for init_target in initialization_tasks:
            tg.create_task(init_target())
