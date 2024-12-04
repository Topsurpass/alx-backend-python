from mysql.connector import errorcode
import mysql.connector
from decimal import Decimal

# Ensure the function is defined at the module level
def stream_users():
    """
    Generator function to fetch rows one by one from the user_data table.
    Yields:
        Dict: A row from the user_data table.
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
        for row in cursor:
            yield row 
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
