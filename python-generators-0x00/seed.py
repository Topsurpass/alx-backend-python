import csv
import mysql.connector
from mysql.connector import errorcode
import uuid

# Function to connect to MySQL Server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="Temz",
            password="Temitope_12",
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="Temz",
            password="Temitope_12",
            database="ALX_prodev",
            port=3306
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
        """)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to insert data into the table
def insert_data(connection, file_path):
    try:
        # Read CSV file
        data = []
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        
        # Insert into database
        cursor = connection.cursor()
        for row in data:
            # Check if the email already exists
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
            if cursor.fetchone() is None:  # Only insert if email is not found
                user_id = str(uuid.uuid4())
                cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
