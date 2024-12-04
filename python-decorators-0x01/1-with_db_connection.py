import sqlite3
import functools

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

@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a user by user_id."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == '__main__':
    user = get_user_by_id(user_id='c57d0a9e-c69e-4601-8a98-1e553be4e0d1')
    if user:
        print(user)
    else:
        print("User not found or an error occurred.")
