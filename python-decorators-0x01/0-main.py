#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_to_db()
if connection:
    print(f"connection successful")

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()