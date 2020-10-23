import sqlite3 as sl
import os
from dotenv import load_dotenv

load_dotenv()

db = sl.connect("andy.db")
cur = db.cursor()
cur.execute("CREATE TABLE diary(mood int, entry varchar(5000), dt datetime, last_edited datetime);")
cur.execute("CREATE TABLE todo(title varchar(200), description varchar(5000), priority int, status boolean);")
print("Tables created successfully!")