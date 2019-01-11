#!/usr/bin/python
from Tkinter import *

# https://stackoverflow.com/questions/14946963/tkinter-grid-how-to-position-widgets-so-they-are-not-stuck-together

class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        self.main_container = Frame(parent)
        self.main_container.grid(row=0, rowspan=2, column=0, columnspan=4)

        self.top_frame = Frame(self.main_container)
        self.top_frame.grid(row=0, column=0, columnspan=4)

        self.top_left = Frame(self.top_frame)
        self.top_left.grid(row=0, column=0, columnspan=2)

        self.top_right = Frame(self.top_frame)
        self.top_right.grid(row=0, column=2, columnspan=2)

        self.bottom_frame = Frame(self.main_container)
        self.bottom_frame.grid(row=2, column=0, columnspan=4)

        self.top_left_label = Label(self.top_left, text="Top Left")
        self.top_left_label.grid(row=0, column=0, sticky='W', padx=2, pady=2)

        self.top_right_label = Label(self.top_right, text="Top Right")
        self.top_right_label.grid(row=0, column=4, sticky='E', padx=2, pady=2)

        self.text_box = Text(self.bottom_frame, height=5, width=40)
        self.text_box.grid(row=0, column=0)

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()