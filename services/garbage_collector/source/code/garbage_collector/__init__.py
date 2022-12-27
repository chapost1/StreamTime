import time
import threading
from .garbage_collector import collect


def collect_garbage_every_x_minutes(minutes: int = 1):
    """Collects garbage every x minutes."""

    delay_in_seconds = int(minutes * 60)

    while True:
        threading.Thread(
            target=collect,
            name=__name__
        ).start()

        time.sleep(delay_in_seconds)
