import mysql.connector as connector


db = connector.connect(host="localhost",
	user="volt",
	password="pj@#9801",
	database="cs_project"
)
cur = db.cursor()


# functions for diary table
def create_entry(mood: int,  entry: str, dt: str):
	cur.execute(f'insert into diary(mood, entry, dt) values({mood}, "{entry}", "{dt}");')
	db.commit()

def fetch_entries(date):
	cur.execute(f"select * from diary where dt like '{date}%' order by dt desc;")
	records = [record for record in cur]
	return records


# functions for todo table
def create_task(title: str, description: str, priority: int):
	cur.execute(f'insert into todo values("{title}", "{description}", {priority}, 0);')
	db.commit()

def fetch_incomplete_tasks():
	cur.execute("select * from todo where status is False;")
	incomplete_tasks = [tasks for tasks in cur]
	return incomplete_tasks

def fetch_completed_tasks():
	cur.execute("select * from todo where status is True;")
	complete_tasks = [tasks for tasks in cur]
	return complete_tasks

def change_status(task, new_status):
	title, description, priority, status = task
	cur.execute(f"update todo set status={new_status} where title='{title}' and description='{description}' and priority={priority} and status={status};")
	db.commit()

def del_task(task):
	title, description, priority, status = task
	cur.execute(f"delete from todo where title='{title}' and description='{description}' and priority={priority} and status={status};")
	db.commit()