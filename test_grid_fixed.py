#!/usr/bin/python
from Tkinter import *

# https://stackoverflow.com/questions/14946963/tkinter-grid-how-to-position-widgets-so-they-are-not-stuck-together

class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        self.main_container = Frame(parent, background="bisque")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.myParent.grid_rowconfigure(0, weight=1)
        self.myParent.grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(self.main_container, background="green")
        self.bottom_frame = Frame(self.main_container, background="yellow")
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.top_left = Frame(self.top_frame, background="pink")
        self.top_right = Frame(self.top_frame, background="blue")
        self.top_left.grid(row=0, column=0, sticky="w")
        self.top_right.grid(row=0, column=2, sticky="e")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.top_left_label = Label(self.top_left, text="Top Left")
        self.top_right_label = Label(self.top_right, text="Top Right")
        self.top_left_label.grid(row=0, column=0, sticky="w")
        self.top_right_label.grid(row=0, column=0, sticky="e")

        self.text_box = Text(self.bottom_frame, height=5, width=40, background="red")
        self.text_box.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()