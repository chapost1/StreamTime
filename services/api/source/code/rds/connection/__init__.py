from rds.connection.connection import Connection
from rds.connection.pool import create_pg_pool
from rds.connection.config import config

async def init() -> None:
    dsn = f'dbname={config["database"]} user={config["user"]} password={config["password"]} host={config["host"]} port={config["port"]}'
    pool = await create_pg_pool(dsn)
    Connection(pool)
