import time
import logging
import schedule
import garbage_collector


logger = logging.getLogger(__name__)


def schedule_gc_job(scheduler: schedule.Scheduler, minutes_interval: int) -> bool:
    """
    Assign the Garbage Collection job to the scheduler.

    Args:
        minutes_interval (int): The interval in minutes to run the job.

    Returns:
        keep_alive (bool): A flag to keep the job scheduler alive.
    """

    if minutes_interval <= 0:
        logger.info('Collection task is chosen to run immidiately...')
        garbage_collector.collect()
        return False

    logger.info(f'Starting job scheduler to run every {minutes_interval} minutes...')
    (
        scheduler
        .every(interval=minutes_interval).minutes
        .do(garbage_collector.collect)
        .tag(garbage_collector.__name__)
    )
    return True



def start(minutes_interval: int = 5) -> None:
    """Start the job scheduler."""

    keep_alive: bool = schedule_gc_job(
        scheduler=schedule,
        # convert the minutes interval to an integer
        minutes_interval=int(minutes_interval)
    )

    while keep_alive:
        schedule.run_pending()
        # check for pending jobs every 30 seconds
        time.sleep(30)


if __name__ == '__main__':
    start(minutes_interval=0)
