
from typing import List, Tuple, Any
from external_systems.data_access.rds.pg.connection.abstract.conncetion import ConnectionProtocol


class ConnectionMock:
    f"""
    Mock Connection client class which supports async operations
    its purpose is to help with pg database unit tests without any side effects

    Abstract protocol docs:
    {ConnectionProtocol.__doc__}
    """

    return_value: Any
    side_effect: Exception


    def __init__(self, return_value: Any = None, side_effect: Exception = None) -> None:
        self.return_value = return_value
        self.side_effect = side_effect


    async def execute(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
        if self.side_effect is not None:
            raise self.side_effect
        return None


    async def query(self, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> List[Tuple]:
        if self.side_effect is not None:
            raise self.side_effect
        return self.return_value
