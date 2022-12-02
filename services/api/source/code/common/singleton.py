import threading

lock = threading.Lock()

class Singleton(type):
    """A Sigleton metaclass to use wether a Singleton class is needed"""

    _instances = {}
    def __call__(cls, *args, **kwargs):
        # double checking lock to prevent performance problems
        # in case the __new__ call of the singleton subclass is called frequently
        # it will keep acquiring locks and will make app slower
        # this approach solves this
        # (the acquire call happens only if a race happens on the first time the singleton is created)
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    def clear(cls):
        try:
            del Singleton._instances[cls]
        except KeyError:
            pass
