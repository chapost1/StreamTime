import time
from typing import Optional
import threading
from .producer import Producer
from .config import producer_steps


def scan_garbage_every(
    minutes: Optional[int] = None,
    seconds: Optional[int] = None
):
    """Scans garbage every x seconds."""

    if seconds is not None:
        # if seconds is specified, ignore minutes
        delay_in_seconds = seconds
    elif minutes is not None:
        # if minutes is specified, convert to seconds
        delay_in_seconds = int(minutes * 60)
    else:
        # default delay is 1 minute
        delay_in_seconds = 60

    # start the scan job
    while True:
        threading.Thread(
            target=Producer().workflow,
            args=(producer_steps,),
            name=__name__
        ).start()

        time.sleep(delay_in_seconds)
