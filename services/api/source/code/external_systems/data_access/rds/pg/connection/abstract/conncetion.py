
from typing import List, Tuple, Any, Protocol


class ConnectionProtocol(Protocol):
    """Connection class Protocol"""
    
    async def execute(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
        """Executes sql statement"""

    async def query(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> List[Tuple]:
        """Returns records returned by sql query"""
