from external_systems.data_access.rds.pg.connection.connection import Connection
from external_systems.data_access.rds.pg.connection.pool import create_pg_pool
from external_systems.data_access.rds.pg.connection.config import config


async def init() -> None:
    """Initialize the Singleton PG client using the async pg pool"""

    dsn = f'dbname={config["database"]} user={config["user"]} password={config["password"]} host={config["host"]} port={config["port"]}'
    pool = await create_pg_pool(dsn)

    Connection(pool)


async def terminate() -> None:
    """Terminates the Singleton PG client"""

    await Connection().clear()
