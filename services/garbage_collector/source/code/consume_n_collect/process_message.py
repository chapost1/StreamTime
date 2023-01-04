from shared.models.garbage.garbage import Garbage
from shared.models.bag.bagger import Bagger
from shared.models.bag.bag import GarbageBag
from typing import Awaitable, Optional
import logging

logger = logging.getLogger(__name__)


async def on_message(garbage: Garbage, done: Awaitable[Optional[Exception]]) -> None:
    """Collects garbage."""
    try:
        garbage_bag: GarbageBag = Bagger.bag(garbage=garbage)

        await garbage_bag.collect()
    except Exception as exc:
        await done(exc)
        logger.error(f'Error while collecting garbage, {exc}')
    else:
        await done(None)
        logger.info(f'Collected garbage: {garbage}')
