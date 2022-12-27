import job_scheduler
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(asctime)s >> %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p %Z'
)


if __name__ == '__main__':
    # start the job scheduler
    job_scheduler.start()
