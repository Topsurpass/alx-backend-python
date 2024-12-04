#!/usr/bin/python3

fetch_all_users = __import__('0-log_queries').fetch_all_users

users = fetch_all_users(query="SELECT * FROM users")
print(users)
