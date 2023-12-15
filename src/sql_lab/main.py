import psycopg2
import psycopg2.extras
from sql_lab import generate_data
import pandas as pd


def load_secret() -> tuple[str]:
	with open("src/sql_lab/secret.txt") as F:
		user = F.readline().rstrip()
		password = F.readline().rstrip()
	return (user, password)


def create_table(cursor):
	DROP_IF_EXISTS_QUERY = """
	DROP TABLE IF EXISTS orders
	"""
	cursor.execute(DROP_IF_EXISTS_QUERY)

	CREATE_TABLE_QUERY = """
	CREATE TABLE IF NOT EXISTS orders (
		id SERIAL PRIMARY KEY,
		user_id VARCHAR(16),
		order_id VARCHAR(16),
		order_time BIGINT,
		order_cost REAL,
		success_order_flg BOOLEAN
	)
	"""
	cursor.execute(CREATE_TABLE_QUERY)


def insert_data(cursor):
	INSERT_QUERY = """
	INSERT INTO orders
	(user_id, order_id, order_time, order_cost, success_order_flg)
	VALUES %s
	"""

	data = generate_data.generate_data()
	# data = generate_data.generate_test()
	template = "(%(user_id)s, %(order_id)s, %(order_time)s, %(order_cost)s, %(success_order_flg)s)"

	psycopg2.extras.execute_values(cur=cursor,
								sql=INSERT_QUERY, 
								argslist=data, 
								template=template)
	

def delete_data(cursor):
	DELETE_QUERY = """
	TRUNCATE TABLE orders
	"""
	cursor.execute(DELETE_QUERY)


def select_data(cursor) -> tuple[list]:
	with open("src/sql_lab/select.sql") as F:
		SELECT_QUERY = F.read().rstrip()
	cursor.execute(SELECT_QUERY)
	return cursor.fetchall(), [x[0] for x in cursor.description]
 

def main():
	user, password = load_secret()
	
	db_params = {
		'database': 'lab',
		'user': user,
		'password': password,
		'host': '127.0.0.1',
		'port': '5432',
	}

	conn = psycopg2.connect(**db_params)

	cursor = conn.cursor()

	# create_table(cursor=cursor)
	# conn.commit()
	# delete_data(cursor=cursor)
	# conn.commit()
	# insert_data(cursor=cursor)
	# conn.commit()
	array, columns = select_data(cursor=cursor)
	conn.commit()
	
	cursor.close()
	conn.close()

	df = pd.DataFrame(data=array, columns=columns)
	print(df)


if __name__ == "__main__":
	main()
