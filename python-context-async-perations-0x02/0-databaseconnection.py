import sqlite3

class DatabaseConnection(object):
    """
    A context manager for managing SQLite database connections.

    This class simplifies the process of establishing, using, and closing
    connections to an SQLite database by leveraging Python's context management
    protocol (`with` statement). It ensures that the connection is closed
    automatically when the block is exited, even in the event of an exception.

    Attributes:
        conn (sqlite3.Connection): The SQLite database connection object.
    """

    def __init__(self, db_name):
        """
        Initializes the DatabaseConnection instance with the specified database name.

        :param db_name: The name of the SQLite database file to connect to.
        """
        self.conn = sqlite3.connect(db_name)

    def __enter__(self):
        """
        Enters the context of the DatabaseConnection instance.

        :return: The SQLite connection object.
        """
        return self.conn

    def __exit__(self, type, value, traceback):
        """
        Exits the context of the DatabaseConnection instance, ensuring the connection
        is properly closed and handling any exceptions that occurred.

        :param type: The exception type, if an exception occurred.
        :param value: The exception value, if an exception occurred.
        :param traceback: The traceback object, if an exception occurred.
        :return: True if an exception occurred (to suppress it), otherwise None.
        """
        self.conn.close()
        if type is not None:
            print(f"Error: {value}")
        return True  # Suppress exceptions


if __name__ == '__main__':
    """
    Example usage of the DatabaseConnection context manager.

    This example connects to an SQLite database named 'users.db', executes
    a query to retrieve all rows from a table named 'users', and prints the
    results. The database connection is automatically closed after the query.
    """
    with DatabaseConnection('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        print(cursor.fetchall())
