from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
from datetime import datetime

import db


class Andy(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.minsize(500, 500)
		self.title("Andy - Diary & To-Do")
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		# container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for frame_page in (Homescreen, DiaryFrame, DiaryCreateFrame):
			page_name = frame_page.__name__
			frame = frame_page(parent=container, controller=self)
			self.frames[page_name] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("Homescreen")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()



class Homescreen(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		global andy, diary_img, todo_img

		andy_img = Image.open("assets/Andy.png").resize((313, 252), Image.ANTIALIAS)
		andy = ImageTk.PhotoImage(andy_img)
		image = Label(self, image=andy, text="Hii, my name is Andy, your personal diary and to-do app. ^_^", compound="top")
		image.pack()

		diary_img = ImageTk.PhotoImage(Image.open("assets/diary.png").resize((60, 60), Image.ANTIALIAS))
		diary_btn = Button(self, text="Diary", image=diary_img, anchor="center", height=100, width=100, compound="top", bd=0, command=lambda: controller.show_frame("DiaryFrame"))
		diary_btn.pack(side="left", expand=True, anchor="e", padx=(0, 50))

		todo_img = ImageTk.PhotoImage(Image.open("assets/todo.png").resize((60, 60), Image.ANTIALIAS))
		todo_btn = Button(self, text="To-Do", image=todo_img, anchor="center", height=100, width=100, compound="top", bd=0)
		todo_btn.pack(side="right", expand=True, anchor="w", padx=(50, 0))


class DiaryFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		global back_img, create_img

		back_img = ImageTk.PhotoImage(Image.open("assets/back.png"))
		back_btn = Button(self, text="Back to Menu", image=back_img, anchor="center", compound="left", bd=0, padx=-10, command=lambda: controller.show_frame("Homescreen"))
		back_btn.pack(pady=(0,20))

		image = Label(self, image=diary_img, text="Diary", compound="left", padx=10)
		image.pack()

		diary_help = Label(self, text="Use the diary to store your thoughts or narrate how your day went.\nDon't worry, Andy is great at keeping secrets ;]")
		diary_help.pack(pady=10)

		create_img = ImageTk.PhotoImage(Image.open("assets/create.png").resize((50, 50), Image.ANTIALIAS))
		create_btn = Button(self, text="Create new entry", image=create_img, anchor="center", compound="left", bd=0, command=lambda: controller.show_frame("DiaryCreateFrame"))
		create_btn.pack(pady=20)

	def check_records(self):
		pass


class DiaryCreateFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
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
			time = datetime.now()
			date_label.configure(text=time.strftime('%d'))
			month_label.configure(text=time.strftime('%b'))
			day_label.configure(text=time.strftime('%a'))
			time_label.configure(text=time.strftime('%H:%M:%S'))
			time_label.after(100, tick)

		tick()

		self.mood_label = Label(self, text="How did your day go?", anchor="w")
		self.mood_label.grid(row=3, column=0, sticky='nesw', padx=25, columnspan=5, pady=(30, 0))

		self.var = IntVar()
		mood_1 = ImageTk.PhotoImage(Image.open("assets/mood-1.png").resize((30, 30), Image.ANTIALIAS))
		mood_2 = ImageTk.PhotoImage(Image.open("assets/mood-2.png").resize((30, 30), Image.ANTIALIAS))
		mood_3 = ImageTk.PhotoImage(Image.open("assets/mood-3.png").resize((30, 30), Image.ANTIALIAS))
		mood_4 = ImageTk.PhotoImage(Image.open("assets/mood-4.png").resize((30, 30), Image.ANTIALIAS))
		mood_5 = ImageTk.PhotoImage(Image.open("assets/mood-5.png").resize((30, 30), Image.ANTIALIAS))

		mood_1_btn = Radiobutton(self, image=mood_1, variable=self.var, value=1, bd=0, anchor="w").grid(row=4, column=0, sticky='nesw', padx=25)
		mood_2_btn = Radiobutton(self, image=mood_2, variable=self.var, value=2, bd=0, anchor="w").grid(row=4, column=1, sticky='nesw', padx=25)
		mood_3_btn = Radiobutton(self, image=mood_3, variable=self.var, value=3, bd=0, anchor="w").grid(row=4, column=2, sticky='nesw', padx=25)
		mood_4_btn = Radiobutton(self, image=mood_4, variable=self.var, value=4, bd=0, anchor="w").grid(row=4, column=3, sticky='nesw', padx=25)
		mood_5_btn = Radiobutton(self, image=mood_5, variable=self.var, value=5, bd=0, anchor="w").grid(row=4, column=4, sticky='nesw', padx=25)

		# self.title = StringVar()
		# title_label = Label(self, text="Title", anchor="w").grid(row=3, column=0, sticky='nesw', padx=25, pady=(25, 0), columnspan=5)
		# title_field = Entry(self, textvariable=self.title).grid(row=4, column=0, sticky='nesw', padx=25, pady=(0,20), columnspan=5)

		self.entry_label = Label(self, text="Entry", anchor="w")
		self.entry_label.grid(row=6, column=0, sticky='nesw', padx=25, columnspan=5)
		self.entry_field = ScrolledText(self, height=10, width=10)
		self.entry_field.grid(row=7, column=0, sticky='nesw', padx=25, pady=(0,20), columnspan=5)

		save_img = ImageTk.PhotoImage(Image.open("assets/save.png").resize((25, 25), Image.ANTIALIAS))
		save_btn = Button(self, text="Save entry", image=save_img, anchor="center", compound="left", bd=0, command=lambda: self.save_entry())
		save_btn.grid(pady=20, columnspan=5)

	def save_entry(self):
		if self.var.get() == 0 or self.entry_field.get("1.0", "end-1c") == "":
			if self.var.get() == 0:
				self.mood_label.configure(text="How did your day go? [*Please select an option]")
			if self.entry_field.get("1.0", "end-1c") == "":
				self.entry_label.configure(text="Entry [*Please type something here]")
		else:
			self.mood_label.configure(text="How did your day go?")
			self.entry_label.configure(text="Entry")

			present_time = datetime.now()
			ftime = present_time.strftime("%Y-%m-%d %H:%M:%S")
			db.create_entry(self.var.get(), self.entry_field.get("1.0", "end-1c"), ftime)

			self.var.set(0)
			self.entry_field.delete("1.0", "end-1c")



if __name__ == "__main__":
	app = Andy()
	app.mainloop()
