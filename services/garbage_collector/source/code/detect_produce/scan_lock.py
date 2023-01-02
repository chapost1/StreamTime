import os
import logging
import threading
import pathlib
from enum import Enum
import atexit

logger = logging.getLogger(__name__)

# only one scanner can run at a time
# and scan jobs are not thread safe
# so we lock it with a file


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
    Lock the Producer Scan operation.

    Returns:
        is_locked (bool): A flag to indicate if the scanner is already locked.
    """

    # acquire the lock
    thread_safe_resource_lock.acquire()

    # check if the scanner is already locked
    if os.path.exists(get_lock_path()):
        with open(get_lock_path(), 'r+b') as lock_file:
            lock = lock_file.read()
            if lock == binary_lock_status(LockStatus.LOCKED):
                logger.info('The scanner is already locked.')
                # release the lock
                thread_safe_resource_lock.release()

                # we are locked
                return True
    
    logger.info('Locking the scanner...')

    with open(get_lock_path(), 'wb') as lock_file:
        lock_file.write(binary_lock_status(LockStatus.LOCKED))

    # release the lock
    thread_safe_resource_lock.release()

    # we are not locked
    return False


def unlock() -> None:
    """Unlock the scanner."""
    logger.info('Unlocking the scanner...')

    # acquire the lock
    thread_safe_resource_lock.acquire()
    
    with open(get_lock_path(), 'wb') as lock_file:
        lock_file.write(binary_lock_status(LockStatus.UNLOCKED))

    # release the lock
    thread_safe_resource_lock.release()


# register the unlock function to be called when the program exits
# safely unlock the scanner
# in case the program exits unexpectedly
atexit.register(unlock)
