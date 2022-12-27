import logging


logger = logging.getLogger(__name__)


def collect() -> None:
    """Collect garbage from the database."""
    logger.info('Collecting garbage...')
    # TODO: implement logic
    pass


if __name__ == '__main__':
    collect()
