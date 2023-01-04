from shared.rds import handle_connection
import logging


async def init():
    """
    Initialize the garbage collector service.
    Initialize the app dependencies.
    """
    logging.info('Initializing garbage collector service')

    # Initialize the RDS pool
    await handle_connection()
