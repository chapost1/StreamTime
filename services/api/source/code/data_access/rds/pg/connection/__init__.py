from data_access.rds.pg.connection.connection import Connection
from data_access.rds.pg.connection.pool import create_pg_pool
from data_access.rds.pg.connection.config import config

async def init() -> None:
    dsn = f'dbname={config["database"]} user={config["user"]} password={config["password"]} host={config["host"]} port={config["port"]}'
    pool = await create_pg_pool(dsn)
    Connection(pool)
