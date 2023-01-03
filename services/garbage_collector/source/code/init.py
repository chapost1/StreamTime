from shared.rds import handle_connection
import logging


def init():
    """Initialize the garbage collector service."""
    logging.info('Initializing garbage collector service')

    # Initialize app dependencies

    # Initialize the RDS pool
    handle_connection()
