from common.singleton import Singleton
from threading import Lock
import logging
from typing import List
from shared.models.garbage.garbage import Garbage
from shared import queue_integration as queue
from .models import ScanToTaskStepConfig


logger = logging.getLogger(__name__)


class Producer(metaclass=Singleton):
    """Detects garbage and produces tasks for the workers"""

    __slots__ = (
        '_locked',
        '_lock'
    )


    def __init__(self):
        self._locked = False
        self._lock = Lock()


    def workflow(self, configured_steps: List[ScanToTaskStepConfig]) -> None:
        """
        Scans the database for garbage
        And produces tasks for the workers
        """

        if self.lock():
            # the producer scan job is already running
            logger.info('Skipping producer garbage scan...')
            return

        message = 'Producer garbage scan worflow...'

        logger.info(f'[START] {message}')

        for step_config in configured_steps:
            self.scan_and_produce_tasks(
                step_config=step_config
            )
        
        logger.info(f'[END] {message}')

        self.unlock()


    def scan_and_produce_tasks(self, step_config: ScanToTaskStepConfig) -> None:
        """
        Scans the database for garbage
        And produces tasks for the workers
        """

        step_message = f'Scanning {step_config.garbage_type}...'

        logger.info(f'[START] {step_message}')

        garbages: List[Garbage] = step_config.detect_garbage_fn()

        logger.info(f'Found {len(garbages)} {step_config.garbage_type}.')

        for garbage in garbages:
            queue.publish(garbage=garbage)

        logger.info(f'[END] {step_message}')


    def lock(self) -> bool:
        """
        Locks the producer scan process
        Returns False if the lock was acquired
        Returns True if the lock was already acquired
        """

        self._lock.acquire()

        if self._locked:
            logger.info('The producer scan process is already locked.')

            self._lock.release()

            return True

        logger.info('Locking the producer scan process...')

        self._locked = True

        self._lock.release()

        return False


    def unlock(self) -> None:
        """
        Unlocks the producer scan process
        """
        self._lock.acquire()

        logger.info('Unlocking the producer...')

        self._locked = False

        self._lock.release()
