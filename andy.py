from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkcalendar import Calendar, DateEntry
from PIL import ImageTk, Image
from datetime import datetime
import time

import db


class Andy(Tk):
	def __init__(self):
		Tk.__init__(self)
		global andy

		self.minsize(500, 500)
		andy = ImageTk.PhotoImage(Image.open("assets/Andy.png").resize((313, 252), Image.ANTIALIAS))
		self.iconphoto(False, andy)
		self.title("Andy - Diary & To-Do")
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# creating the frames for the app
		self.frames = {}
		for frame_page in (Homescreen, DiaryFrame, DiaryCreateFrame, EntryListFrame, TodoFrame, TaskCreateFrame, TaskEditFrame):
			page_name = frame_page.__name__
			frame = frame_page(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("Homescreen")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()

	def update_entry_list(self, date):
		'''method to update EntryListFrame with the date'''
		frame = self.frames["EntryListFrame"]
		frame.load_content(date)

	def update_task_list(self):
		'''method to update variables in TodoFrame'''
		frame = self.frames["TodoFrame"]
		frame.load_tasks()

	def edit_task_frame(self, task):
		'''method to update variables in TaskEditFrame'''
		frame = self.frames["TaskEditFrame"]
		frame.load_data(task)


class Homescreen(Frame):
	'''The Homescreen Frame which is the first frame of the app and contains the menu'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		global diary_img, todo_img

		inner_frame = Frame(self)
		inner_frame.pack(anchor="center", pady=(30, 0))

		image = Label(inner_frame, image=andy, text="Hii, my name is Andy, your personal diary and to-do app. ^_^", compound="top")
		image.grid(row=0, column=0, columnspan=2, pady=(0,10))

		diary_img = ImageTk.PhotoImage(Image.open("assets/diary.png").resize((60, 60), Image.ANTIALIAS))
		diary_btn = Button(inner_frame, text="Diary", image=diary_img, anchor="center", height=100, width=100, compound="top", bd=0, command=lambda: controller.show_frame("DiaryFrame"))
		diary_btn.grid(row=1, column=0)

		todo_img = ImageTk.PhotoImage(Image.open("assets/todo.png").resize((60, 60), Image.ANTIALIAS))
		todo_btn = Button(inner_frame, text="To-Do", image=todo_img, anchor="center", height=100, width=100, compound="top", bd=0, command=lambda: self.load_todo_frame())
		todo_btn.grid(row=1, column=1)

	def load_todo_frame(self):
		self.controller.update_task_list()  # updates vars in todo frame
		self.controller.show_frame("TodoFrame")


class DiaryFrame(Frame):
	'''DiaryFrame: the frame where the user can create and view diary entries created for a particular day'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.parent = parent

		global back_img, create_img

		back_img = ImageTk.PhotoImage(Image.open("assets/back.png"))
		back_btn = Button(self, text="Back to Menu", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: controller.show_frame("Homescreen"))
		back_btn.pack(pady=(0,20))

		image = Label(self, image=diary_img, text="Diary", compound="left", padx=10)
		image.pack()

		diary_help = Label(self, text="Use the diary to store your thoughts or narrate how your day went.\nDon't worry, Andy is great at keeping secrets ;]")
		diary_help.pack(pady=10)

		create_img = ImageTk.PhotoImage(Image.open("assets/create.png").resize((30, 30), Image.ANTIALIAS))
		create_btn = Button(self, text="Create new entry", image=create_img, anchor="center", compound="left", bd=0, command=lambda: controller.show_frame("DiaryCreateFrame"))
		create_btn.pack(pady=(10, 20))

		cal = Calendar(self, firstweekday="sunday", showweeknumbers=False, borderwidth=0, date_pattern="yyyy-mm-dd")
		cal.pack(padx=20, pady=10)
		print_btn = Button(self, text="Check Entries for the selected date", bd=0, command=lambda: self.check_records(cal.get_date()))
		print_btn.pack(padx=10, pady=10)

	def check_records(self, date):
		global entries
		entries = db.fetch_entries(date)  # fetches the entries created on 'date'
		self.controller.update_entry_list(date)
		self.controller.show_frame("EntryListFrame")


class DiaryCreateFrame(Frame):
	'''Frame for user to create a diary entry'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		# self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, weight=1)
		self.grid_columnconfigure(3, weight=1)
		self.grid_columnconfigure(4, weight=1)

		global back_img, save_img, mood_1, mood_2, mood_3, mood_4, mood_5

		back_btn = Button(self, text="Back", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: controller.show_frame("DiaryFrame"))
		back_btn.grid(row=0, column=0, columnspan=5, pady=(0, 20))

		date_label = Label(self, font=('calibri', 40), anchor="e")
		month_label = Label(self, anchor="w")
		day_label = Label(self, anchor="w")
		time_label = Label(self, font=('calibri', 20), anchor="w")

		date_label.grid(row=1, column=1, sticky='nesw', rowspan=2)
		month_label.grid(row=1, column=2, sticky='nesw')
		day_label.grid(row=2, column=2, sticky='nesw')
		time_label.grid(row=1, column=3, sticky='nesw', rowspan=2)


		def tick():
			'''method to update the time shown in the Frame at regular intervals'''
			time = datetime.now()
			date_label.configure(text=time.strftime('%d'))
			month_label.configure(text=time.strftime('%b'))
			day_label.configure(text=time.strftime('%a'))
			time_label.configure(text=time.strftime('%H:%M:%S'))
			time_label.after(100, tick)

		tick()

		self.mood_label = Label(self, text="How you feeling today?*", anchor="w")
		self.mood_label.grid(row=3, column=0, sticky='nesw', padx=25, columnspan=5, pady=(30, 0))

		self.var = IntVar()
		mood_1 = ImageTk.PhotoImage(Image.open("assets/mood-1.png").resize((30, 30), Image.ANTIALIAS))
		mood_2 = ImageTk.PhotoImage(Image.open("assets/mood-2.png").resize((30, 30), Image.ANTIALIAS))
		mood_3 = ImageTk.PhotoImage(Image.open("assets/mood-3.png").resize((30, 30), Image.ANTIALIAS))
		mood_4 = ImageTk.PhotoImage(Image.open("assets/mood-4.png").resize((30, 30), Image.ANTIALIAS))
		mood_5 = ImageTk.PhotoImage(Image.open("assets/mood-5.png").resize((30, 30), Image.ANTIALIAS))

		mood_1_btn = Radiobutton(self, image=mood_1, variable=self.var, value=1, bd=0, anchor="w").grid(row=4, column=0, sticky='nsw', padx=25)
		mood_2_btn = Radiobutton(self, image=mood_2, variable=self.var, value=2, bd=0, anchor="w").grid(row=4, column=1, sticky='nsw', padx=25)
		mood_3_btn = Radiobutton(self, image=mood_3, variable=self.var, value=3, bd=0, anchor="w").grid(row=4, column=2, sticky='nsw', padx=25)
		mood_4_btn = Radiobutton(self, image=mood_4, variable=self.var, value=4, bd=0, anchor="w").grid(row=4, column=3, sticky='nsw', padx=25)
		mood_5_btn = Radiobutton(self, image=mood_5, variable=self.var, value=5, bd=0, anchor="w").grid(row=4, column=4, sticky='nsw', padx=25)

		self.entry_label = Label(self, text="Entry*", anchor="w")
		self.entry_label.grid(row=6, column=0, sticky='nesw', padx=25, columnspan=5)
		self.entry_field = ScrolledText(self, height=10, width=10)
		self.entry_field.grid(row=7, column=0, sticky='nesw', padx=25, pady=(0,20), columnspan=5)

		save_img = ImageTk.PhotoImage(Image.open("assets/save.png").resize((25, 25), Image.ANTIALIAS))
		save_btn = Button(self, text="Save entry", image=save_img, anchor="center", compound="left", bd=0, command=lambda: self.save_entry())
		save_btn.grid(row=8, column=0, sticky='nesw', pady=20, columnspan=5)

	def save_entry(self):
		'''Method to save the diary entry created by the user'''
		if self.var.get() == 0 or self.entry_field.get("1.0", "end-1c") == "":
			if self.var.get() == 0:
				self.mood_label.configure(text="How you feeling today?* [Please select an option]")
			if self.entry_field.get("1.0", "end-1c") == "":
				self.entry_label.configure(text="Entry* [Please type something here]")
		else:
			self.mood_label.configure(text="How did your day go?")
			self.entry_label.configure(text="Entry*")

			present_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			db.create_entry(self.var.get(), self.entry_field.get("1.0", "end-1c"), present_time)

			# resetting variables
			self.var.set(0)
			self.entry_field.delete("1.0", "end-1c")

			global entries

			date = present_time.split(' ')[0]
			entries = db.fetch_entries(date)
			self.controller.update_entry_list(date)
			self.controller.show_frame("EntryListFrame")


class EntryListFrame(Frame):
	'''Method to view all entries created by user on a particular date'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.pack_propagate(False)

		back_btn = Button(self, text="Back", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: self.show_prev_frame())
		back_btn.pack(pady=(0, 20))

	def load_content(self, date):
		'''method to load all entries created on the date passed as parameter'''
		try:
			self.destroy_all()
		except:
			pass

		self.canvas = Canvas(self)
		self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
		inner_frame = Frame(self.canvas)
		inner_frame.pack(fill="both", expand=True)
		self.canvas.create_window(0, 0, anchor='center', window=inner_frame, width=self.winfo_width(), height=self.winfo_height())

		self.date = date
		year, month, day = self.date.split('-')
		date_label = Label(inner_frame, text=f'Date: {day}-{month}-{year}', anchor="center", bd=0, padx=10, pady=10, font=('calibri', 16)).pack()

		create_btn = Button(inner_frame, text="Add another entry?", image=create_img, anchor="center", compound="left", bd=0, command=lambda: self.controller.show_frame("DiaryCreateFrame")).pack(pady=10)

		# creating labels for each entry or showing "No entries were created for this day" if entries don't exist
		emoticons = {1: mood_1, 2: mood_2, 3: mood_3, 4: mood_4, 5: mood_5}
		for entry in entries:
			mood, content, created_at, edited_at = entry
			time_created_label = Label(inner_frame, text=f"[created at {created_at.strftime('%H:%M')}]", image=emoticons[mood], anchor="center", compound="left", bd=0, padx=10).pack(padx=10, pady=(20,0))
			entry_label = Label(inner_frame, text=content, anchor="center", bd=0, wraplength=self.winfo_width()-50).pack(padx=10, pady=(0,20))

		if not entries:
			empty_msg = Label(inner_frame, text="No entries were created for this day", image=emoticons[4], anchor="center", compound="top", bd=0, padx=10, pady=10, wraplength=self.winfo_width()-50)
			empty_msg.pack(pady=50)

		self.canvas.update_idletasks()
		self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=self.scrollbar.set)
		self.canvas.yview_moveto('0.0')
		self.bind("<Configure>", self.on_resize)
		self.canvas.pack(fill="both", side="left", expand=True, anchor="center")
		self.scrollbar.pack(side="right", fill="y")

	def on_resize(self, event):
		# destroying all widgets and reloading content to make it fit properly within the app window
		self.destroy_all()
		self.load_content(self.date)

	def show_prev_frame(self):
		self.destroy_all()
		self.controller.show_frame("DiaryFrame")

	def destroy_all(self):
		'''method to destroy canvas and scrollbar widget in the frame'''
		if self.canvas:
			self.canvas.destroy()
		if self.scrollbar:
			self.scrollbar.destroy()


class TodoFrame(Frame):
	'''Todo Frame for users to create aand view tasks created'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.pack_propagate(False)

		global add_task_img

		back_btn = Button(self, text="Back to Menu", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: controller.show_frame("Homescreen"))
		back_btn.pack(pady=(0,20))

		image = Label(self, image=todo_img, text="Tasks", compound="left", padx=10)
		image.pack()

		todo_help = Label(self, text="Add your daily tasks/chores here and\ncheck them off when you've completed them.")
		todo_help.pack(pady=10)

		add_task_img = ImageTk.PhotoImage(Image.open("assets/todo_add_new.png").resize((30, 30), Image.ANTIALIAS))
		add_task_btn = Button(self, text="Add new task", image=add_task_img, anchor="center", compound="left", bd=0, command=lambda: controller.show_frame("TaskCreateFrame"))
		add_task_btn.pack()

	def load_tasks(self):
		'''method to load all the tasks created'''
		try:
			self.destroy_all()
		except:
			pass

		self.canvas = Canvas(self)
		self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
		task_frame = Frame(self.canvas, height=self.winfo_height()-100)
		task_frame.pack(fill="x", expand=True)
		self.canvas.create_window(0, 0, anchor='center', window=task_frame, width=self.winfo_width())

		priority_colors = ("#00CED1", "#00FA9A", "#FF6347", "#B0C4DE")
		self.incomplete_tasks = sorted(db.fetch_incomplete_tasks(), key=lambda x: x[2])  # sorting tasks by priority value i.e. more important tasks will be visible on top
		if self.incomplete_tasks:
			incomplete_task_label = Label(task_frame, text="Incomplete Tasks", font=('calibri', 16))
			incomplete_task_label.pack(pady=10, padx=(50, 0), anchor="center")
			# creating button for each task that maps to the edit task frame
			for task in self.incomplete_tasks:
				title, description, priority, status = task
				task_btn = Button(task_frame, text=title, bg=priority_colors[priority-1], bd=0, width=25, wraplength=400, justify="left", anchor="w", pady=5, command=lambda task=task: self.get_task(task))
				task_btn.pack(expand=True, padx=(50,0))

			self.completed_tasks = db.fetch_completed_tasks()
			# display completed tasks, if present
			if self.completed_tasks:
				global done_icon
				done_icon = ImageTk.PhotoImage(Image.open("assets/done.png").resize((25, 25), Image.ANTIALIAS))
				completed_task_label = Label(task_frame, text="Completed Tasks", font=('calibri', 16)).pack(padx=(50,0), pady=10, anchor="center")
				for task in self.completed_tasks:
					title, description, priority, status = task
					task_btn = Button(task_frame, text=title, image=done_icon, compound="left", bd=0, width=200, wraplength=400, justify="left", anchor="w", pady=5, command=lambda task=task: self.get_task(task))
					task_btn.pack(expand=True, padx=(50,0))

		else:
			global no_task_img
			no_task_img = ImageTk.PhotoImage(Image.open("assets/no_task.png").resize((340, 160), Image.ANTIALIAS))
			all_complete = Label(task_frame, text="You're all caught up!", image=no_task_img, compound="top", font=('calibri', 16)).pack(padx=(50,0), pady=10)

		self.canvas.update_idletasks()
		self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=self.scrollbar.set)
		self.canvas.yview_moveto('0.0')
		self.bind("<Configure>", self.on_resize)
		self.canvas.pack(fill="both", side="left", expand=True, anchor="center", pady=(0, 20))
		self.scrollbar.pack(side="right", fill="y")

	def on_resize(self, event):
		self.destroy_all()
		self.load_tasks()

	def destroy_all(self):
		if self.canvas:
			self.canvas.destroy()
		if self.scrollbar:
			self.scrollbar.destroy()

	def get_task(self, task):
		self.controller.edit_task_frame(task)
		self.controller.show_frame("TaskEditFrame")


class TaskCreateFrame(Frame):
	'''Task Create Frame for users to create tasks and save them'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		back_btn = Button(self, text="Back", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: self.load_todo_frame())
		back_btn.grid(row=0, column=0, columnspan=2)
		instruction_label = Label(self, text="Add new task here.", font=('calibri', 16)).grid(row=1, column=0, padx=25, columnspan=2)

		self.title = StringVar()
		self.title_label = Label(self, text="Title*", anchor="w")
		self.title_label.grid(row=2, column=0, sticky='nesw', padx=25, pady=(15, 0), columnspan=2)
		title_field = Entry(self, textvariable=self.title).grid(row=3, column=0, sticky='nesw', padx=25, pady=(0,10), columnspan=2)

		description_label = Label(self, text="Description", anchor="w")
		description_label.grid(row=4, column=0, sticky='nesw', padx=25, columnspan=2)
		self.description_field = ScrolledText(self, height=5, width=10)
		self.description_field.grid(row=5, column=0, sticky='nesw', padx=25, pady=(0,20), columnspan=2)

		self.priority_label = Label(self, text="Choose a priority level for this task*", anchor="w")
		self.priority_label.grid(row=6, column=0, sticky='nesw', padx=25, columnspan=2)

		self.priority_value = 0
		self.priority_1_btn = Button(self, text="Important & Urgent\n[Do it now]", bd=0, bg="#80FDFF", fg="gray15", highlightbackground="#80FDFF", disabledforeground="black", pady=10, padx=5, command=lambda: self.disable_self(1))
		self.priority_2_btn = Button(self, text="Important but not Urgent\n[Schedule a time to do it]", bd=0, bg="#90EE90", fg="gray15", highlightbackground="#90EE90", disabledforeground="black", pady=10, padx=5, command=lambda: self.disable_self(2))
		self.priority_3_btn = Button(self, text="Urgent but not Important\n[What can do it for you?]", bd=0, bg="#FF9380", fg="gray15", highlightbackground="#FF9380", disabledforeground="black", pady=10, padx=5, command=lambda: self.disable_self(3))
		self.priority_4_btn = Button(self, text="Neither Important nor Urgent\n[Eliminate it]", bd=0, bg="#A5BCD9", fg="gray15", highlightbackground="#A5BCD9", disabledforeground="black", pady=10, padx=5, command=lambda: self.disable_self(4))

		self.priority_1_btn.grid(row=7, column=0, sticky='nsew', padx=25, pady=5)
		self.priority_2_btn.grid(row=7, column=1, sticky='nsew', padx=25, pady=5)
		self.priority_3_btn.grid(row=8, column=0, sticky='nsew', padx=25, pady=5)
		self.priority_4_btn.grid(row=8, column=1, sticky='nsew', padx=25, pady=5)

		save_btn = Button(self, text="Save task", image=save_img, anchor="center", compound="left", bd=0, command=lambda: self.save_entry())
		save_btn.grid(row=9, column=0, sticky='nesw', padx=25, columnspan=2, pady=10)

	def disable_self(self, pos):
		# disabling the button which has been chosen
		self.btns =[(self.priority_1_btn, "#00CED1", "#80FDFF"), (self.priority_2_btn, "#00FA9A", "#90EE90"), (self.priority_3_btn, "#FF6347","#FF9380"), (self.priority_4_btn, "#B0C4DE", "#A5BCD9")]
		for btn, active_bg_color, bg_color in self.btns:
			if btn == self.btns[pos-1][0]:
				btn.config(state='disabled', bg=active_bg_color, highlightbackground=active_bg_color, bd=1)
				self.priority_value = pos
			else:
				btn.config(state='normal', bg=bg_color, highlightbackground=bg_color, bd=0)

	def save_entry(self):
		'''method to save the diary entry created by user'''
		if self.priority_value == 0 or self.title.get() == "":
			if self.priority_value == 0:
				self.priority_label.configure(text="Choose a priority level for this task* [Please select an option]")
			if self.title.get() == "":
				self.title_label.configure(text="Title* [Please type something here]")
		else:
			self.priority_label.configure(text="Choose a priority level for this task*")
			self.title_label.configure(text="Title*")

			db.create_task(self.title.get(), self.description_field.get("1.0", "end-1c"), self.priority_value)

			# resetting variables
			self.title.set('')
			self.description_field.delete("1.0", "end-1c")
			self.priority_value = 0
			for btn, active_bg_color, bg_color in self.btns:
				btn.config(state='normal', bg=bg_color, highlightbackground=bg_color, bd=0)

			self.load_todo_frame()

	def load_todo_frame(self):
		self.controller.update_task_list()
		self.controller.show_frame("TodoFrame")


class TaskEditFrame(Frame):
	'''Frame to delete tasks and to mark them as completed/incomplete'''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		global delete_icon, completed_icon, incomplete_icon
		delete_icon = ImageTk.PhotoImage(Image.open("assets/delete.png").resize((20, 20), Image.ANTIALIAS))
		completed_icon = ImageTk.PhotoImage(Image.open("assets/completed.png").resize((20, 20), Image.ANTIALIAS))	
		incomplete_icon = ImageTk.PhotoImage(Image.open("assets/incomplete.png").resize((20, 20), Image.ANTIALIAS))

		back_btn = Button(self, text="Back", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: self.load_todo_frame())
		back_btn.grid(row=0, column=0, columnspan=2, pady=(0,20))

		self.title_label = Label(self, font=('calibri', 16), pady=5)
		self.description_label = Label(self, font=('calibri', 12), pady=5)
		self.priority_label = Label(self, font=('calibri', 8, 'bold'), pady=10)
		self.change_status_btn = Button(self, bd=0)
		self.delete_btn = Button(self, text="Delete", bd=0, image=delete_icon, compound="left", anchor="center", bg="#ff5252")

		self.title_label.grid(row=1, column=0, columnspan=2)
		self.description_label.grid(row=2, column=0, columnspan=2)
		self.priority_label.grid(row=3, column=0, columnspan=2)
		self.change_status_btn.grid(row=4, column=0, pady=(30, 0), padx=10, sticky="e")
		self.delete_btn.grid(row=4, column=1, pady=(30, 0), padx=10, sticky="w")

	def load_data(self, task):
		# loading and setting the value of labels
		title, description, priority, status = task
		priority_levels = {1: "Important & Urgent", 2: "Important but not Urgent", 3: "Urgent but not Important", 4: "Neither Important nor Urgent"}
		self.title_label.config(text=f"Title: {title}")
		self.description_label.config(text=f"Description: {description or 'No Description Given'}")
		self.priority_label.config(text=f"Priority Level: {priority}. {priority_levels[priority]}")	

		if status == 0:  # if task is incomplete
			self.change_status_btn.config(text="Mark as Completed", image=completed_icon, compound="left", command=lambda: self.change_item_status(task, 1))
		elif status == 1:  # if task has been already completed_tasks
			self.change_status_btn.config(text="Mark Incomplete", image=incomplete_icon, compound="left", command=lambda: self.change_item_status(task, 0))

		self.delete_btn.config(command=lambda: self.del_item(task))


	def load_todo_frame(self):
		self.controller.update_task_list()
		self.controller.show_frame("TodoFrame")

	def del_item(self, task):
		# deletes the item and loads Todo Frame
		db.del_task(task)
		self.load_todo_frame()

	def change_item_status(self,task, new_status):
		# updates the status of task
		db.change_status(task, new_status)
		task = list(task)
		task[3] = new_status
		self.load_data(task)


if __name__ == "__main__":
	app = Andy()
	app.mainloop()
