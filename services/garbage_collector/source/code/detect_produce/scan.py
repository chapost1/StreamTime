from detect_produce import scan_lock
import logging
from .scan_to_task import (
    scan_and_produce_tasks,
    producer_steps
)


logger = logging.getLogger(__name__)


def scan() -> None:
    """
    Scans the database for garbage
    And produces tasks for the workers
    """

    if scan_lock.lock():
        # the producer scan job is already running
        logger.info('Skipping producer garbage scan...')
        return

    scan_message = 'Producer garbage scan...'

    logger.info(f'[START] {scan_message}')

    for step in producer_steps:
        scan_and_produce_tasks(step_config=step)
    
    logger.info(f'[END] {scan_message}')

    scan_lock.unlock()


if __name__ == '__main__':
    scan()
