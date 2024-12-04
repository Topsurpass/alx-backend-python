from mysql.connector import errorcode
import mysql.connector
from decimal import Decimal

# Ensure the function is defined at the module level
def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows in chuncks/batches from the user_data table.
    Yields:
        List[Dict]: A list of rows from the user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="Temz",
            password="Temitope_12",
            port=3306,
            database="ALX_prodev",
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
        if batch:
            yield batch 
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def batch_processing(batch_size):
    """
    Process each batch of users to filter out those over the age of 25.
    Args:
        batch_size (int): The number of users to fetch in each batch.
    """
    for batch in stream_users_in_batches(batch_size):
      [print(user) for user in batch if user["age"] > 25]