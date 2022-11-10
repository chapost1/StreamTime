import psycopg2
from psycopg2 import pool
from rds.connection.config import config


# def sql_executor(conn: pg_connection, transaction_steps: List[Tuple[str, Tuple[Any]]]) -> None:
#     with conn:
#         with conn.cursor() as cursor:
#             for sql, params in transaction_steps:
#                 cursor.execute(sql, params)

def run_test():
    try:
        postgreSQL_pool = pool.SimpleConnectionPool(2, 20, **config)
        if (postgreSQL_pool):
            print("Connection pool created successfully")

        # Use getconn() to Get Connection from connection pool
        ps_connection = postgreSQL_pool.getconn()

        if (ps_connection):
            print("successfully recived connection from connection pool ")
            ps_cursor = ps_connection.cursor()
            ps_cursor.execute("select * from videos")
            videos = ps_cursor.fetchall()

            print("Displaying rows from videos table")
            for row in videos:
                print(row)

            ps_cursor.close()

            # Use this method to release the connection object and send back to connection pool
            postgreSQL_pool.putconn(ps_connection)
            print("Put away a PostgreSQL connection")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # closing database connection.
        # use closeall() method to close all the active connection if you want to turn of the application
        if postgreSQL_pool:
            postgreSQL_pool.closeall
        print("PostgreSQL connection pool is closed")
