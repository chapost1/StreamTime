from common.environment import INSTANCE_TYPE
from common.enums import InstanceTypes
import detect_n_produce as producer
import consume_n_collect as consumer
from init import init as init_service
import logging
import asyncio


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(asctime)s >> %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p %Z'
)


async def start_worker():
    if INSTANCE_TYPE == InstanceTypes.PRODUCER.value:
        await producer.scan_garbage_every(minutes=1)
    elif INSTANCE_TYPE == InstanceTypes.WORKER.value:
        await consumer.collect()
    else:
        raise Exception(f'Unknown instance type {INSTANCE_TYPE}')


async def main():
    """Main entrypoint for the garbage collector service."""

    # Initialize the service
    await init_service()

    # Start the worker by instance type
    await start_worker()


if __name__ == '__main__':
    asyncio.run(main())
