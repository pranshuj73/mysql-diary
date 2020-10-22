import mysql.connector as connector
import os
from dotenv import load_dotenv

load_dotenv()

db = connector.connect(host="localhost",
	user=os.environ.get('MYSQL_USERNAME'),
	password=os.environ.get('MYSQL_PASSWORD'),
	database="andy"
)
cur = db.cursor()


# functions for diary table
def create_entry(mood: int,  entry: str, dt: str):
	'''method to create new diary entry'''
	cur.execute(f'insert into diary(mood, entry, dt) values({mood}, "{entry}", "{dt}");')
	db.commit()

def fetch_entries(date) -> list:
	'''method to fetch the diary entries for a particular date'''
	cur.execute(f"select * from diary where dt like '{date}%' order by dt desc;")
	records = [record for record in cur]
	return records


# functions for todo table
def create_task(title: str, description: str, priority: int):
	'''method to create new task'''
	cur.execute(f'insert into todo values("{title}", "{description}", {priority}, 0);')
	db.commit()

def fetch_incomplete_tasks() -> list:
	'''method to fetch incomplete tasks from the db and return a list of the tasks'''
	cur.execute("select * from todo where status is False;")
	incomplete_tasks = [tasks for tasks in cur]
	return incomplete_tasks

def fetch_completed_tasks() -> list:
	'''method to fetch completed tasks from the db and return a list of the tasks'''
	cur.execute("select * from todo where status is True;")
	complete_tasks = [tasks for tasks in cur]
	return complete_tasks

def change_status(task, new_status):
	'''updates the status of the task to new_status'''
	title, description, priority, status = task
	cur.execute(f"update todo set status={new_status} where title='{title}' and description='{description}' and priority={priority} and status={status};")
	db.commit()

def del_task(task):
	'''deletes the task from db'''
	title, description, priority, status = task
	cur.execute(f"delete from todo where title='{title}' and description='{description}' and priority={priority} and status={status};")
	db.commit()