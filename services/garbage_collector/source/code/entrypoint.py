from common.environment import INSTANCE_TYPE
from common.enums import InstanceTypes
import detect_n_produce as producer
import consume_n_collect as consumer
from init import init as init_service
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(asctime)s >> %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p %Z'
)


def start_worker():
    if INSTANCE_TYPE == InstanceTypes.PRODUCER.value:
        producer.scan_garbage_every(minutes=1)
    elif INSTANCE_TYPE == InstanceTypes.WORKER.value:
        consumer.work()
    else:
        raise Exception(f'Unknown instance type {INSTANCE_TYPE}')


def main():
    """Main entrypoint for the garbage collector service."""

    # Initialize the service
    init_service()

    # Start the worker by instance type
    start_worker()


if __name__ == '__main__':
    main()
