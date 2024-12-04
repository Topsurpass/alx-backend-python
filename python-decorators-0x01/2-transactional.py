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

def transactional(func):
    @functools.wraps(func)
    def wrapper_transactional(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print('Transaction committed')
            return result
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Transaction rollback: {e}")
            return None
    return wrapper_transactional
        
        
@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
	cursor = conn.cursor() 
	cursor.execute("UPDATE users SET email = ? WHERE user_id = ?", (new_email, user_id)) 
	#### Update user's email with automatic transaction handling 

if __name__ == "__main__":
    update_user_email(user_id='c57d0a9e-c69e-4601-8a98-1e553be4e0d1', new_email='Temitopeabiodun685@gmail.com')