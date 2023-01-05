from shared.models.garbage.garbage import Garbage
from shared.models.bag.bagger import Bagger
from shared.models.bag.bag import GarbageBag
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PostProcessMessage:
    def __call__(self, error: Optional[Exception]) -> None:
        """Mark processing the message as done, and optionally pass an error"""


async def on_message(garbage: Garbage, post_process_message: PostProcessMessage) -> None:
    """Callback for when a message is received from the queue"""
    try:
        # Create a garbage bag and collect the garbage
        garbage_bag: GarbageBag = Bagger.bag(garbage=garbage)

        await garbage_bag.collect()
    except Exception as exc:
        # If there is an error, mark the message as processed with an error
        # and log the error
        await post_process_message(error=exc)
        logger.error(f'Error while collecting garbage, {exc}')
    else:
        # If there is no error, mark the message as processed successfully
        await post_process_message(error=None)
        logger.info(f'Collected garbage: {garbage}')
