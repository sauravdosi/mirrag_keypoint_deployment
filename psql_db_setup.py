import psycopg2
from psycopg2 import Error
from psycopg2.extensions import AsIs
import datetime
import bcrypt

class DatabaseUtil:
	def __init__(self,username,password,hostip,port,database):
		self.username = username
		self.password = password
		self.hostip = hostip
		self.port = port
		self.database = database
		self.connection=self.connect()

	def connect(self):
		if self.check_connection(verbose=True):
			self.connection = psycopg2.connect(user=self.username, #"postgres",
											  password=self.password,#"mirragdb",
											  host=self.hostip,#"127.0.0.1",
											  port=self.port,#"5432",
											  database=self.database)#"test")
		return self.connection
	 
	def check_connection(self,verbose=False):
		connection=None
		flag=True
		try:
			# Connect to an existing database
			connection = psycopg2.connect(user=self.username, #"postgres",
										  password=self.password,#"mirragdb",
										  host=self.hostip,#"127.0.0.1",
										  port=self.port,#"5432",
										  database=self.database)#"test")

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
			flag=False
		finally:
			if (connection is not None):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")
			return flag
			
	def create_tables(self):
		##server_ip VARCHAR(50) NOT NULL,#,	
		commands = (
			"""
			CREATE TABLE intrusiontben (image_index BIGSERIAL NOT NULL PRIMARY KEY,
						  company_id VARCHAR(50) NOT NULL,
						  cam_id INT NOT NULL,
						  company_name VARCHAR(100) NOT NULL,
						  model_version VARCHAR(50) NOT NULL,
						  violation_flag bool NOT NULL,
						  file_path VARCHAR(500) NOT NULL,
						  out_data jsonb NOT NULL,
						  pred_time TIMESTAMP NOT NULL,
						  created_time TIMESTAMP NOT NULL,
						  description VARCHAR(200))
			""",
			""" CREATE TABLE companytben1 (
						 company_id SERIAL NOT NULL PRIMARY KEY,
						 company_name VARCHAR(50) NOT NULL,
						 company_code VARCHAR(50) NOT NULL,
						 auth_key VARCHAR(200) NOT NULL)
			""")

		cursor = self.connection.cursor()
		for command in commands:
			try:
				print("Ab")
				cursor.execute(command)
			except psycopg2.errors.DuplicateTable:
				continue
		self.connection.commit()
		cursor.close()

	def set_password(self,pw):
		pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
		password_hash = pwhash.decode('utf8')
		return password_hash

	def insert_record(self, db_table, rec: dict,encode_password=False):
		if encode_password==True:
			password_hash = self.set_password(rec["password"])
			del rec["password"]
			rec["auth_key"] = password_hash
		columns = rec.keys()
		values = [rec[column] for column in columns]

		insert_statement = 'insert into {} (%s) values %s'.format(db_table)
		cursor = self.connection.cursor()
		cursor.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
		self.connection.commit()
		cursor.close()


if __name__=="__main__":
	print("Running PSQL_DB Script to create tables")
	dbobj=DatabaseUtil("postgres","mirragdb","127.0.0.1","5432","mirragdatabase")
	dbobj.create_tables()
	print("Successful")
