from .pool import Pool
from .config import config
import asyncio_atexit


async def init_rds_pool():
    pool = Pool(config=config)
    await pool.open()


async def terminate_rds_pool():
    pool = Pool()
    await pool.close()


async def handle_connection():
    # It will initialize the pool and register the termination function
    # The termination function will be called when the main thread is terminated
    # The termination function will close the pool
    # The pool will be closed only once

    # Initialize the pool
    await init_rds_pool()

    # Register the termination function
    asyncio_atexit.register(terminate_rds_pool)
