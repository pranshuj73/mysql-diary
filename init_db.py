import mysql.connector as connector
import os

db = connector.connect(host="localhost",
	user=os.environ.get('MYSQL_USERNAME'),
	password=os.environ.get('MYSQL_PASSWORD')
)
cur.execute("CREATE DATABASE andy;")

db = connector.connect(host="localhost",
	user=os.environ.get('MYSQL_USERNAME'),
	password=os.environ.get('MYSQL_PASSWORD'),
	database="andy"
)
cur = db.cursor()
cur.execute("CREATE TABLE diary(mood int, entry varchar(5000), dt datetime, last_edited datetime);")
cur.execute("CREATE TABLE todo(title varchar(200), description varchar(5000), priority int, status boolean);")