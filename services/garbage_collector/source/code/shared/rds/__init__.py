from .pool import Pool
import atexit


def init_rds_pool():
    pool = Pool()
    pool.open()


def terminate_rds_pool():
    pool = Pool()
    pool.close()


def handle_connection():
    # This function is called from the main thread
    # It will be called only once
    # It will initialize the pool and register the termination function
    # The termination function will be called when the main thread is terminated
    # The termination function will close the pool
    # The pool will be closed only once

    # Initialize the pool
    init_rds_pool()

    # Register the termination function
    atexit.register(terminate_rds_pool)
