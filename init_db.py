import mysql.connector as connector

# db = connector.connect(host="localhost",
# 	user="volt",
# 	password="pj@#9801"
# )



# cur.execute("CREATE DATABASE andy;")

db = connector.connect(host="localhost",
	user="volt",
	password="pj@#9801",
	database="cs_project"
)
cur = db.cursor()
cur.execute("CREATE TABLE diary(mood int, entry varchar(5000), dt datetime, last_edited datetime);")
# cur.execute("CREATE TABLE todo(title int, notes varchar(5000), deadline datetime, status int);")