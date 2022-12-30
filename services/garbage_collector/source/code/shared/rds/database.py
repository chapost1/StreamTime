import psycopg2
from shared.rds.config import config
from shared.garbage.garbage import Garbage
from typing import Protocol

# The database queries are happening once in a while
# So we don't need to keep the connection open
# We can open a connection, execute the query and close the connection

class GarbageFactory(Protocol):
    def create(self, **kwargs) -> Garbage:
        ...


class Database:

    __slots__ = (
        'garbage_factory',
        'connection',
        'cursor'
    )


    def __init__(self, garbage_factory: GarbageFactory):
        self.garbage_factory = garbage_factory
        self.reset()


    def begin(self):
        self.connection = psycopg2.connect(**config)
        self.connection.autocommit = False
        self.cursor = self.connection.cursor()
    

    def execute(self, query: str, params: tuple = None):
        self.cursor.execute(query, params)
    

    def fetchone(self):
        return self.cursor.fetchone()
    

    def fetchall(self):
        return self.cursor.fetchall()


    def commit(self):
        self.connection.commit()
        self.connection.close()
        self.reset()


    def rollback(self):
        self.connection.rollback()
        self.connection.close()
        self.reset()
    

    def reset(self):
        self.cursor = None
        self.connection = None