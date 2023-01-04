import aiopg
from typing import Dict
from common.singleton import Singleton
from threading import Lock


class Pool(metaclass=Singleton):

    __slots__ = [
        'dsn',
        '_lock',
        '_pool'
    ]


    def __init__(self, config: Dict[str, str]):
        self.dsn = f"host={config['host']} port={config['port']} dbname={config['database']} user={config['user']} password={config['password']}"
        self._pool = None
        self._lock = Lock()


    async def open(self):
        self._lock.acquire()
        if self._pool is not None:
            return

        try:
            pool: aiopg.Pool = await aiopg.create_pool(
                dsn=self.dsn,
                minsize=1,
                maxsize=25
            )
            if (pool):
                print('Connection pool created successfully')
            else:
                message = 'Connection pool creation failed'
                raise Exception(message)
        except Exception as error:
            print('Error while connecting to PostgreSQL', error)
            self._lock.release()
            raise Exception('Failed to initialize pg connection')

        self._pool = pool
        self._lock.release()
    

    async def close(self):
        self._lock.acquire()
        self._pool.terminate()
        await self._pool.wait_closed()
        self._pool = None
        self._lock.release()


    @property
    def transaction_ctx(self) -> aiopg.Pool:
        if self._pool is None:
            raise RuntimeError('Pool is not initialized')
        return self._pool.acquire
