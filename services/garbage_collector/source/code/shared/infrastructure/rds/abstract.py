from typing import Protocol, Any, Awaitable, Optional
import aiopg


class Database(Protocol):
    """Abstract class for database connections"""

    @property
    def transaction(self) -> Any:
        """
        returns context manager for acquiring connection
        every action will be executed in the same transaction
        """


    async def dml(self, action: Awaitable, connection: Optional[aiopg.Connection]) -> Any:
        """
        Executes a DML query
        If connection is None, it will open a new connection
        Otherwise, it will use the provided connection
        """
