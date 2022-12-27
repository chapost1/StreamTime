import logging
import garbage_collector.lock as collection_lock


logger = logging.getLogger(__name__)


def collect() -> None:
    """Collect garbage from the database."""

    if collection_lock.lock():
        logger.info('Skipping garbage collection...')
        return

    logger.info('Collecting garbage...')


    # TODO: implement logic


    collection_lock.unlock()


if __name__ == '__main__':
    collect()
