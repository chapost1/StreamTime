from typing import Any
import aiopg

async def create_pg_pool(dsn: str) -> Any:
    print(dsn)
    try:
        pool = await aiopg.create_pool(dsn, minsize=1, maxsize=20)
        if (pool):
            print('Connection pool created successfully')
    except Exception as error:
        print('Error while connecting to PostgreSQL', error)
        raise Exception('Failed to initialize pg connection')
    return pool
