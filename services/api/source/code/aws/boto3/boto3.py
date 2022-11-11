
from common.singleton import Singleton
from aiobotocore.session import AioSession


class Boto3(metaclass=Singleton):
    __slots__ = (
        '__session',
    )

    def __init__(self, session=None) -> None:
        if session is None:
            raise Exception('No Session')
        self.__session = session
    
    def session(self) -> AioSession:
        return self.__session
