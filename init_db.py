import mysql.connector as connector
import os
from dotenv import load_dotenv

load_dotenv()

db = connector.connect(host="localhost",
	user=os.environ.get('MYSQL_USERNAME'),
	password=os.environ.get('MYSQL_PASSWORD')
)
cur = db.cursor()
cur.execute("CREATE DATABASE andy;")
print("Database created successfully!")

db = connector.connect(host="localhost",
	user=os.environ.get('MYSQL_USERNAME'),
	password=os.environ.get('MYSQL_PASSWORD'),
	database="andy"
)
cur = db.cursor()
cur.execute("CREATE TABLE diary(mood int, entry varchar(5000), dt datetime, last_edited datetime);")
cur.execute("CREATE TABLE todo(title varchar(200), description varchar(5000), priority int, status boolean);")
print("Tables created successfully!")