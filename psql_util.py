import psycopg2
from psycopg2.extensions import AsIs
import bcrypt
import datetime

class DatabaseUtil:
	def __init__(self, username, password, hostip, port, database):
		self.username = username
		self.password = password
		self.hostip = hostip
		self.port = int(port)
		self.database = database
		self.connection = self.connect()

	def connect(self):
		if self.	check_connection(verbose=False):
			self.connection = psycopg2.connect(user=self.username,  # "postgres",
											   password=self.password,  # "mirragdb",
											   host=self.hostip,  # "127.0.0.1",
											   port=self.port,  # "5432",
											   database=self.database)  # "test")
		return self.connection

	def check_connection(self, verbose=False):
		connection = None
		flag = True
		try:
			# Connect to an existing database
			connection = psycopg2.connect(user=self.username,  # "postgres",
										  password=self.password,  # "mirragdb",
										  host=self.hostip,  # "127.0.0.1",
										  port=self.port,  # "5432",
										  database=self.database)  # "test")

			# Create a cursor to perform database operations
			cursor = connection.cursor()
			# Print PostgreSQL details
			if verbose:
				print("PostgreSQL server information")
				print(connection.get_dsn_parameters(), "\n")
				# Executing a SQL query
				cursor.execute("SELECT version();")
				# Fetch result
				record = cursor.fetchone()
				print("You are connected to - ", record, "\n")
		except (Exception, Error) as error:
			print("Error while connecting to PostgreSQL", error)
			flag = False
		finally:
			if (connection is not None):
				cursor.close()
				connection.close()
				print("Database connection is established.")
			return flag

	# def page_not_found(e):
	# 	return "<h1>404</h1><p>The resource could not be found.</p>", 404

	def read_records(self):
		cursor = self.connection.cursor()

		cursor.execute("SELECT * FROM testtb")
		all_data = cursor.fetchall()
		cursor.close()
		return all_data

	def auth_check(self, rec: dict):
		# fields = ', '.join(rec.keys())
		# values = ', '.join(['%%(%s)s' % x for x in rec])
		# query = 'INSERT INTO some_table %s VALUES %s' % (fields, values)
		# cursor.execute(query, rec)

		auth_flag = False
		# query = "SELECT auth_key FROM companytb WHERE company_id = '{0}'".format(str(rec["id"]))
		query = "SELECT auth_key FROM companytben WHERE company_code = '{0}'".format(str(rec["code"]))
		cursor = self.connection.cursor()
		cursor.execute(query)
		authkey_db = cursor.fetchall()
		password=rec["authkey"].encode('utf-8')
		if len(authkey_db)>0:
			hashed=authkey_db[0][0]
			if bcrypt.checkpw(password, hashed.encode("utf-8")):
				auth_flag = True
		return auth_flag

	def read_filter_records(self,query_parameters):

		id = query_parameters.get('cam_id')
		published = query_parameters.get('published')
		author = query_parameters.get('company_name')

		query = 'SELECT * FROM intrusiontb WHERE'
		to_filter = []

		if id:
			query += ' cam_id=%s AND'
			to_filter.append(id)
		if published:
			query += ' published=%s AND'
			to_filter.append(published)
		if author:
			query += ' company_name=%s AND'
			to_filter.append(author)

		query = query[:-4] + ';'

		cursor = self.connection.cursor()
		cursor.execute(query, to_filter)
		results = cursor.fetchall()
		return results

	def insert_record(self, rec: dict, db_table):
		"""Inserts a record into given table"""
		try:
			rec["created_time"] = datetime.datetime.now()
			columns = rec.keys()
			values = [rec[column] for column in columns]

			insert_statement = 'INSERT INTO {} (%s) VALUES %s'.format(db_table)
			# Create a cursor to perform database operations
			cursor = self.connection.cursor()
			cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
			self.connection.commit()
			cursor.close()
		except Exception as e:
			# @TODO log a msg with error
			return False
		return True

