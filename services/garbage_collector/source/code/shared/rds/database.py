from .pool import Pool
import aiopg
from typing import Awaitable, Any, Optional

# The database queries are happening once in a while
# So we don't need to keep the connection open
# We can open a connection, execute the query and close the connection


class Database:

    @property
    def transaction(self) -> Any:
        """
        returns context manager for acquiring connection
        every action will be executed in the same transaction
        """
        return Pool().transaction_ctx()


    async def dml(self, action: Awaitable, connection: Optional[aiopg.Connection]) -> Any:
        """
        Executes a DML query
        If connection is None, it will open a new connection
        Otherwise, it will use the provided connection
        """
        if connection is None:
            async with self.transaction as connection:
                return await action(cursor=await connection.cursor())
        else:
            return await action(cursor=await connection.cursor())
