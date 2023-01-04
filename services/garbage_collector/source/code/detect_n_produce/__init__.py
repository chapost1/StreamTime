from typing import Optional
import time
from .producer import Producer
from .config import producer_steps
import asyncio
import logging

logger = logging.getLogger(__name__)


def get_delay_in_seconds(
    minutes: Optional[int] = None,
    seconds: Optional[int] = None
) -> int:
    """Returns the delay in seconds."""

    if seconds is not None:
        # if seconds is specified, ignore minutes
        return seconds
    elif minutes is not None:
        # if minutes is specified, convert to seconds
        return int(minutes * 60)
    else:
        # default delay is 1 minute
        return 60


async def infinite_scan(delay_in_seconds: int):
    """Infinitely scans garbage."""

    while True:
        scan_start_ts = time.time()
        try:
            await Producer().workflow(configured_steps=producer_steps)
        except Exception as exc:
            # log the exception instead of crashing the service
            logger.error(f'Producer generated an exception: {exc}')
        else:
            logger.info(f'Producer scan job completed.')
        
        # if an exception is raised, then we will reach this line
        # and we will wait for the remaining time
        elapsed = time.time() - scan_start_ts
        remaining = delay_in_seconds - elapsed
        if remaining > 0:
            await asyncio.sleep(remaining)


async def scan_garbage_every(
    minutes: Optional[int] = None,
    seconds: Optional[int] = None
):
    """Scans garbage every x seconds."""

    # start the scan job
    await infinite_scan(
        delay_in_seconds=get_delay_in_seconds(
            minutes=minutes,
            seconds=seconds
        )
    )
