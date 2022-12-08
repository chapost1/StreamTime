from typing import Protocol
from external_systems.data_access.rds.pg.connection.abstract.conncetion import ConnectionProtocol

class GetConnectionFunction(Protocol):
    def __call__(self) -> ConnectionProtocol:
        """
        returns connection, using function as a factory to ensure the connection is already initailized
        because concrete implementation may be a singleton which is not initialized on app load
        
        it is safer to pass the factory instead of instance in case the singleton class reference is not valid anymore/yet
        """
