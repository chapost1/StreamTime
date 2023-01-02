from common.environment import INSTANCE_TYPE
from common.enums import InstanceTypes
import detect_produce
import consume_collect
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(asctime)s >> %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p %Z'
)


def main():
    """Main entrypoint for the garbage collector service."""

    if INSTANCE_TYPE == InstanceTypes.PRODUCER.value:
        detect_produce.scan_garbage_every(seconds=10)
    elif INSTANCE_TYPE == InstanceTypes.WORKER.value:
        consume_collect.work()
    else:
        raise Exception(f'Unknown instance type {INSTANCE_TYPE}')


if __name__ == '__main__':
    main()
