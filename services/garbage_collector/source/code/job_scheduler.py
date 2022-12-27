import time
import schedule
import garbage_collector


def start(minutes_interval: int = 5) -> None:
    """Start the job scheduler."""

    # convert the minutes interval to an integer
    minutes_interval = int(minutes_interval)

    # no need to run the job scheduler
    if minutes_interval <= 0:
        print('Collection task is chosen to run immidiately...')
        garbage_collector.collect()
        return

    print(f'Starting job scheduler to run every {minutes_interval} minutes...')
    # assign the job to the scheduler
    # to run every x minutes
    (
        schedule
        .every(interval=minutes_interval).minutes
        .do(garbage_collector.collect)
        .tag(garbage_collector.__name__)
    )

    # run the scheduler
    while True:
        schedule.run_pending()
        # check for pending jobs every 30 seconds
        time.sleep(30)


if __name__ == '__main__':
    start(minutes_interval=0)
