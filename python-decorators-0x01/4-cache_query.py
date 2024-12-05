import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to manage database connection."""
    @functools.wraps(func)
    def wrapper_db_connection(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            print(f"Connection successful")
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                conn.close()
                print(f"Connection closed")
    return wrapper_db_connection

def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        query = kwargs.get('query') or args[1]
        if query in query_cache:
            print('Data retrieved from cache')
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper_cache


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == '__main__':
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)