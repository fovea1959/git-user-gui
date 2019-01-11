#!/usr/bin/python
from Tkinter import *

# https://stackoverflow.com/questions/14946963/tkinter-grid-how-to-position-widgets-so-they-are-not-stuck-together

class MyApp:
    def __init__(self, parent):
        self.myParent = parent
        self.main_container = Frame(parent, background="bisque")
        self.main_container.pack(side="top", fill="both", expand=True)

        self.top_frame = Frame(self.main_container, background="green")
        self.bottom_frame = Frame(self.main_container, background="yellow")
        self.top_frame.pack(side="top", fill="x", expand=False)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)

        self.top_left = Frame(self.top_frame, background="pink")
        self.top_right = Frame(self.top_frame, background="blue")
        self.top_left.pack(side="left", fill="x", expand=True)
        self.top_right.pack(side="right", fill="x", expand=True)

        self.top_left_label = Label(self.top_left, text="Top Left")
        self.top_right_label = Label(self.top_right, text="Top Right")
        self.top_left_label.pack(side="left")
        self.top_right_label.pack(side="right")

        self.text_box = Text(self.bottom_frame, height=5, width=40, background="red")
        self.text_box.pack(side="top", fill="both", expand=True)

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()