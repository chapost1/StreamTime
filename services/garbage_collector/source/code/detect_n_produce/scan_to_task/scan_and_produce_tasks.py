import logging
from typing import List
from shared.models.garbage.garbage import Garbage
from shared import queue_integration as queue
from .models import ScanToTaskStepConfig


logger = logging.getLogger(__name__)


def scan_and_produce_tasks(step_config: ScanToTaskStepConfig) -> None:
    """
    Scans the database for garbage
    And produces tasks for the workers
    """

    step_message = f'Scanning {step_config.garbage_type}...'

    logger.info(f'[START] {step_message}')

    garbages: List[Garbage] = step_config.detect_garbage_fn()

    for garbage in garbages:
        queue.publish(garbage=garbage)

    logger.info(f'[END] {step_message}')
