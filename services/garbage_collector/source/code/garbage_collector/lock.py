import os
import logging
import threading
import pathlib
from enum import Enum
import atexit

logger = logging.getLogger(__name__)

# TODO: fixme to use a better lock
# i.e: redis distributed cluster
# so that we can have multiple instances of the garbage collector
# running at the same time
# and they will be able to lock/unlock the garbage collector
# without any issues

# thread safe resource lock
thread_safe_resource_lock = threading.Lock()


class LockStatus(str, Enum):
    """The lock status."""
    LOCKED = 'LOCKED'
    UNLOCKED = 'UNLOCKED'


def get_lock_path() -> str:
    """Get the lock file path."""
    return os.path.join(pathlib.Path(__file__).parent.absolute(), 'lock.bin')


def lock() -> bool:
    """
    Lock the garbage collector.

    Returns:
        is_locked (bool): A flag to indicate if the garbage collector is already locked.
    """

    # acquire the lock
    thread_safe_resource_lock.acquire()

    # check if the garbage collector is already locked
    if os.path.exists(get_lock_path()):
        with open(get_lock_path(), 'r+') as lock_file:
            lock = lock_file.read()
            if lock == str(LockStatus.LOCKED.value):
                logger.info('The garbage collector is already locked.')
                # release the lock
                thread_safe_resource_lock.release()

                # we are locked
                return True
    
    logger.info('Locking the garbage collector...')

    with open(get_lock_path(), 'w') as lock_file:
        lock_file.write(LockStatus.LOCKED.value)

    # release the lock
    thread_safe_resource_lock.release()

    # we are not locked
    return False


def unlock() -> None:
    """Unlock the garbage collector."""
    logger.info('Unlocking the garbage collector...')

    # acquire the lock
    thread_safe_resource_lock.acquire()
    
    with open(get_lock_path(), 'w') as lock_file:
        lock_file.write(LockStatus.UNLOCKED.value)

    # release the lock
    thread_safe_resource_lock.release()


# register the unlock function to be called when the program exits
# safely unlock the garbage collector
# in case the program exits unexpectedly
atexit.register(unlock)
