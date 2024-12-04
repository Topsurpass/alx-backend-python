#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
	"""Pagenate user_data table in the db

	Args:
		page_size (number): data size to return per page
		offset (number): number to start querying from for next page

	Returns:
		List[Dict]: List of rows in Dict format
	"""
	connection = seed.connect_to_prodev()
	cursor = connection.cursor(dictionary=True)
	cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
	rows = cursor.fetchall()
	connection.close()
	return rows

def lazy_paginate(pagesize):
	"""Simulte fetching paginated data from the users database using a generator to lazily load each page

	Args:
		page_size (number): data size to return per page

	Yields:
		List[Dict]: List of rows in Dict format
	"""
	offset = 0
	while True:
		current_page = paginate_users(pagesize, offset)
		if not current_page:
			break
		yield current_page
		offset += pagesize