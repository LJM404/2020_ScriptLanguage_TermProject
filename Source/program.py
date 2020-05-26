from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from graphBox import GraphBox


class Program:
    def __init__(self):
        self.window = Tk()
        self.window.title("거기 공기 어때?")
        self.window.geometry("750x300") # 종횡비( 2.5:1 )
        self.window.resizable(False, False)
        self.initialize()
        self.window.mainloop()
        pass

    def initialize(self):
        self.font = font.Font()

        # 왼쪽 프레임
        self.leftFrame = ttk.LabelFrame(self.window, text="대기오염정보")
        self.leftFrame.place(x=20, y=10, width=350, height=270)

        # 오른쪽 프레임
        self.rightFrame = ttk.LabelFrame(self.window, text="그래프")
        self.rightFrame.place(x=380, y=10, width=350, height=270)

        # 그래프 박스
        self.graphBox = GraphBox(self.rightFrame, x=5, y=0, width=330, height=200)
        self.graphBox.updateGraph()
        pass