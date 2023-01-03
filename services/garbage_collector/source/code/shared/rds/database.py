from .pool import Pool

# The database queries are happening once in a while
# So we don't need to keep the connection open
# We can open a connection, execute the query and close the connection


class Database:

    __slots__ = (
        'connection',
        'cursor'
    )


    def __init__(self):
        self.connection = None
        self.cursor = None


    def begin(self):
        self.retain_connection()
    

    def execute(self, query: str, params: tuple = None):
        self.cursor.execute(query, params)
    

    def fetchone(self):
        return self.cursor.fetchone()
    

    def fetchall(self):
        return self.cursor.fetchall()


    def commit(self):
        self.connection.commit()
        self.release_connection()


    def rollback(self):
        self.connection.rollback()
        self.release_connection()
    

    def retain_connection(self):
        self.connection = Pool().get_connection()
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
    

    def release_connection(self):
        self.cursor = None
        Pool().release_connection(self.connection)
        self.connection = None
