import logging
import garbage_collector.lock as collection_lock
import time

logger = logging.getLogger(__name__)


def collect() -> None:
    """
    Collect garbage from the database
    And remove it from the different stores.
    """

    if collection_lock.lock():
        logger.info('Skipping garbage collection...')
        return

    logger.info('Collecting garbage...')


    # TODO: implement logic
    time.sleep(5)
    


    collection_lock.unlock()


if __name__ == '__main__':
    collect()
