from typing import Protocol

class Storage(Protocol):
    @staticmethod
    def get_client():
        """
        returns the client to interact with the storage
        """
