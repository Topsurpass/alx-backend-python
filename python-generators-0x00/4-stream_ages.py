from mysql.connector import errorcode
import mysql.connector
from decimal import Decimal

# Ensure the function is defined at the module level
def stream_user_ages():
    """
    Generator function to fetch user age from rows one by one from the user_data table.
    Yields:
        Dict: A row from the user_data table containing only the age.
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
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            age = row['age']
            yield age 
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def calculate_avg_age():
	"""Using generator to compute a memory-efficient aggregate function i.e average age for a large dataset

	Returns:
		string: Avegrage age of users
	"""
	total_age = 0
	num_of_users = 0

	for age in stream_user_ages():
		total_age += age
		num_of_users += 1
		if num_of_users == 0:
			return f"Average age of users: 0"
	average_age = total_age / num_of_users
	return f"Average age of users: {average_age:.2f}"               