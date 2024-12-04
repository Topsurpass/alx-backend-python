import csv
import sqlite3
import uuid

# Function to connect to SQLite database
def connect_to_db(db_name="users.db"):
    try:
        connection = sqlite3.connect(db_name)
        return connection
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL
        )
        """)
        connection.commit()
    except sqlite3.Error as err:
        print(f"Error: {err}")

def insert_data(connection, file_path):
    try:
        # Read CSV file
        data = []
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)

        # Insert data into the database
        cursor = connection.cursor()
        for row in data:
            # Check if the email already exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (row['email'],))
            if cursor.fetchone() is None:  # Only insert if email is not found
                user_id = str(uuid.uuid4())
                cursor.execute("""
                INSERT INTO users (user_id, name, email, age)
                VALUES (?, ?, ?, ?)
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except sqlite3.Error as err:
        print(f"Error: {err}")
