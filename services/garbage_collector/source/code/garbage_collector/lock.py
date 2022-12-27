import os
import logging
import threading
import pathlib
from enum import Enum
import atexit

logger = logging.getLogger(__name__)

# the garbage collector is a long running task
# altough this task is important, it is not critical to occur at a specific time.
# therefore there will be only one instance of the garbage collector running at a time.
# Since the collect task is scheduled to run every x minutes, it is possible that multiple instances of the task will be triggered concurrently.
# it may be possible that the garbage collector is already running (did not finish the previous trigger) when the task is triggered.
# to prevent this, we will use a lock file to indicate if the garbage collector is already running.
# if the garbage collector is already running, we will not run it again.


# thread safe resource lock
thread_safe_resource_lock = threading.Lock()

class LockStatus(str, Enum):
    """The lock status."""
    LOCKED = 1
    UNLOCKED = 0


def binary_lock_status(lock_status: LockStatus) -> bytes:
    """Get the binary lock status."""
    return bytearray(str(lock_status.value), encoding='utf-8')


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
        with open(get_lock_path(), 'r+b') as lock_file:
            lock = lock_file.read()
            if lock == binary_lock_status(LockStatus.LOCKED):
                logger.info('The garbage collector is already locked.')
                # release the lock
                thread_safe_resource_lock.release()

                # we are locked
                return True
    
    logger.info('Locking the garbage collector...')

    with open(get_lock_path(), 'wb') as lock_file:
        lock_file.write(binary_lock_status(LockStatus.LOCKED))

    # release the lock
    thread_safe_resource_lock.release()

    # we are not locked
    return False


def unlock() -> None:
    """Unlock the garbage collector."""
    logger.info('Unlocking the garbage collector...')

    # acquire the lock
    thread_safe_resource_lock.acquire()
    
    with open(get_lock_path(), 'wb') as lock_file:
        lock_file.write(binary_lock_status(LockStatus.UNLOCKED))

    # release the lock
    thread_safe_resource_lock.release()


# register the unlock function to be called when the program exits
# safely unlock the garbage collector
# in case the program exits unexpectedly
atexit.register(unlock)
