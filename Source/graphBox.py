from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class GraphBox:
    def __init__(self, master, x, y, width, height, bg="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.canvas = Canvas(master=master, width=width, height=height, bg=bg)
        self.canvas.place(x=x, y=y)
        pass

    def updateGraph(self, left=50, right=10, top=10, bottom=20):
        self.canvas.delete("all")

        # x축, y축 그리기
        self.canvas.create_line(left, self.height-bottom, self.width-right, self.height-bottom)
        self.canvas.create_line(left, top, left, self.height - bottom)

        self.canvas.update()
        pass