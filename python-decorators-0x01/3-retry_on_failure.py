import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""
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

def retry_on_failure(retries=3, delay=1):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    attempts += 1
                    print(f"Attempt {attempts}/{retries} failed: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper_retry
    return decorator_retry


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)