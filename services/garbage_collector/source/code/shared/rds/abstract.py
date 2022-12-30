from typing import Protocol

class Database(Protocol):
    """Abstract class for database connections"""


    def begin(self):
        """Opens a connection and creates a cursor"""
    

    def execute(self, query: str, params: tuple = None):
        """Executes a query"""
    

    def fetchone(self):
        """Fetches one row"""
    

    def fetchall(self):
        """Fetches all rows"""


    def commit(self):
        """Commits the transaction and closes the connection"""


    def rollback(self):
        """Rolls back the transaction and closes the connection"""
