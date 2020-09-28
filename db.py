import mysql.connector as connector


db = connector.connect(host="localhost",
	user="volt",
	password="pj@#9801",
	database="cs_project"
)
cur = db.cursor()


# functions for diary table
def create_entry(mood: int,  entry: str, dt: str):
	cur.execute(f'INSERT INTO diary(mood, entry, dt) values({mood}, "{entry}", "{dt}");')
	db.commit()

def fetch_entries():
	cur.execute("select * from diary;")
	records = [record for record in cur]
	return records

