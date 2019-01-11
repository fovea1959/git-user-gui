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
        self.middle_frame = Frame(self.main_container, background="orange")
        self.bottom_frame = Frame(self.main_container, background="yellow")
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.middle_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_frame.grid(row=2, column=0, sticky="ew")
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

        self.button = Button(self.middle_frame, text="Set", background="red")
        self.button.grid(row=0, column=0)
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)


        self.bottom_left = Frame(self.bottom_frame, background="pink")
        self.bottom_right = Frame(self.bottom_frame, background="blue")
        self.bottom_left.grid(row=0, column=0, sticky="w")
        self.bottom_right.grid(row=0, column=2, sticky="e")
        self.bottom_frame.grid_columnconfigure(1, weight=1)


        self.bottom_left_label = Label(self.bottom_left, text="Top Left")
        self.bottom_right_label = Label(self.bottom_right, text="Top Right")
        self.bottom_left_label.grid(row=0, column=0, sticky="w")
        self.bottom_right_label.grid(row=0, column=0, sticky="e")

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()