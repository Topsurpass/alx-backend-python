import sqlite3

class ExecuteQuery(object):
    """
    A context manager for executing SQL queries on an SQLite database.

    This class facilitates managing SQLite database connections and executing
    SQL queries with parameters. It ensures the connection and cursor are 
    properly closed after use, even if an exception occurs.

    Attributes:
        db_name (str): The name of the SQLite database file.
        query (str): The SQL query to execute.
        params (tuple): Parameters for the SQL query.
        connection (sqlite3.Connection): The database connection object.
        cursor (sqlite3.Cursor): The database cursor for executing queries.
    """

    def __init__(self, db_name, query, params):
        """
        Initializes the ExecuteQuery instance with the database name, query, and parameters.

        :param db_name: Name of the SQLite database file to connect to.
        :param query: SQL query to be executed.
        :param params: Parameters for the SQL query.
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Enters the context of the ExecuteQuery instance by establishing a database connection.

        :return: Self to execute the query.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def execute_query(self):
        """
        Executes the SQL query with the provided parameters.

        :return: List of tuples containing the query results.
        """
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, type, value, traceback):
        """
        Exits the context of the ExecuteQuery instance, closing the cursor and connection.

        :param type: The exception type, if an exception occurred.
        :param value: The exception value, if an exception occurred.
        :param traceback: The traceback object, if an exception occurred.
        :return: True if an exception occurred (to suppress it), otherwise None.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if type is not None:
            print(f"Error: {value}")
        return True  # Suppress exceptions


if __name__ == '__main__':
    """
    Example usage of the ExecuteQuery context manager.

    This example connects to an SQLite database named 'users.db', executes
    a parameterized query to fetch users older than a specified age, and prints
    the results. The database connection and cursor are automatically closed
    after the query.
    """
    query = "SELECT * FROM users WHERE age > ?"
    params = (105,)

    with ExecuteQuery('users.db', query, params) as executor:
        results = executor.execute_query()
        print(results)
