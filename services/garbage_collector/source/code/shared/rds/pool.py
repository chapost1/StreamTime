from psycopg_pool import ConnectionPool
from shared.rds.config import config
from common.singleton import Singleton


class Pool(metaclass=Singleton):

    __slots__ = [
        '_pool'
    ]


    def __init__(self):
        conninfo = f"host={config['host']} port={config['port']} dbname={config['database']} user={config['user']} password={config['password']}"

        self._pool = ConnectionPool(
            min_size=1,
            max_size=10,
            open=False,
            conninfo=conninfo
        )


    def open(self):
        self._pool.open()
    

    def close(self):
        self._pool.close()


    def get_connection(self):
        return self._pool.getconn()


    def release_connection(self, conn):
        self._pool.putconn(conn)
