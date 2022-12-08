
from common.singleton import Singleton
from external_systems.data_access.rds.pg.connection.abstract.conncetion import ConnectionProtocol
from typing import List, Tuple, Any, Union
import aiopg


class Connection(metaclass=Singleton):
    f"""
    Singleton PG Connection client class which supports async operations

    It uses connection pool to avoid TCP hand-shake on every database operation

    Abstract protocol docs:
    {ConnectionProtocol.__doc__}
    """

    __slots__ = (
        'pool'
    )

    def __init__(self, pool: aiopg.Pool = None) -> None:
        if pool is None:
            raise Exception('No PG connection')
        self.pool = pool
    
    async def clear(self) -> None:
        print('pg connetcion pool delete has been called...')

        if self.pool is None:
            print('connection pool is None')
        else:
            print('terminating pg...')            
            self.pool.terminate()
            await self.pool.wait_closed()
            print('pg terminated...')
            del self.pool

        print('clears singleton instance')
        Singleton.clear(self.__class__)

    async def __transaction(self, cursor, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
        for sql, params in transaction_steps:
            if params is None:
                params = tuple([])
            await cursor.execute(sql, params)

    async def __execute(self, transaction_steps: List[Tuple[str, Tuple[Any]]], query=False) -> Union[None, List[Tuple]]:
        handled = False
        ret = None
        try:
            with (await self.pool.cursor()) as cursor:
                try:
                    await self.__transaction(cursor, transaction_steps)
                    if query:
                        ret = await cursor.fetchall()
                except Exception as e:
                    message = 'Error while performing transaction'
                    print(message, e)
                    cursor.execute('rollback')
                    handled = True
                    raise Exception(e)

        except Exception as e:
            if handled:
                raise e
            message = 'Error while trying to get a cursor from pool'
            print(message, e)
            raise Exception(message)

        return ret
    
    async def execute(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
        await self.__execute(transaction_steps=transaction_steps)

    async def query(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> List[Tuple]:
        return await self.__execute(transaction_steps=transaction_steps, query=True)
