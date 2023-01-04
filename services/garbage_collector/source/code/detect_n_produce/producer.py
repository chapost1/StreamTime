from common.singleton import Singleton
import logging
from typing import List
from shared.models.garbage.garbage import Garbage
from shared import queue_integration as queue
from .models import ScanToTaskStepConfig
import asyncio


logger = logging.getLogger(__name__)


class Producer(metaclass=Singleton):
    """Detects garbage and produces tasks for the workers"""


    async def workflow(self, configured_steps: List[ScanToTaskStepConfig]) -> None:
        """The producer scan job workflow"""

        message = 'Producer garbage scan worflow...'

        logger.info(f'[START] {message}')

        tasks = [self.execute_step(step_config=step_config) for step_config in configured_steps]

        await asyncio.gather(*tasks)

        logger.info(f'[END] {message}')


    async def execute_step(self, step_config: ScanToTaskStepConfig) -> None:
        """
        Scans the database for garbage
        And produces tasks for the workers
        """

        step_message = f'Scanning {step_config.garbage_type}...'

        logger.info(f'[START] {step_message}')

        garbages: List[Garbage] = await step_config.detect_garbage_fn()

        published_count = await self.publish_tasks(garbages=garbages)

        logger.info(f'Poducer Published {published_count}/{len(garbages)} tasks.')

        logger.info(f'[END] {step_message}')
    

    async def publish_tasks(self, garbages: List[Garbage]) -> int:
        """Publishes tasks for the workers"""

        published_count: int = 0
        # publish tasks for each garbage
        tasks = [queue.publish(garbage) for garbage in garbages]
        try:
            # wait for all tasks to complete
            result: List[bool] = await asyncio.gather(*tasks)
            # reduce result to count of published tasks
            # count true values
            published_count = sum(result)
        except Exception as exc:
            # should not happen
            # but if it does, log the exception
            logger.error(f'Producer generated an exception: {exc}')

        return published_count
