import math, sys
from ctypes import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def extractFromData(data, key, xLabel, ny, r):
    xAxis, yAxis, values = [], [], []
    
    if (data is None) or (len(data) == 0):
        return xAxis, yAxis, values
    
    for it in data:
        if it[key] is not None:
            xAxis.append(it[xLabel])
            values.append(it[key])
    
    print("debug message: origin - ", data)
    print("debug message: extract - ", values)
    if len(values) == 0:
        return xAxis, yAxis, values


    minimum, maximum = min(values), max(values)
    if math.fabs(maximum - minimum) <= sys.float_info.epsilon or ny <= 1:
        yAxis.insert(0, minimum)
    else:
        for i in range(ny):
            yAxis.insert(0, round(minimum + i * (maximum - minimum) / (ny - 1), r))

    return xAxis, yAxis, values


class GraphBox:
    def __init__(self, master, x, y, width, height, bg="white"):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.canvas = Canvas(master=master, width=width, height=height, bg=bg)
        self.canvas.place(x=x, y=y)

        # C++로 작성된 동적라이브러리의 함수 연결
        clib = cdll.LoadLibrary("./Module/calcModule.dll")
        self.getDataPointPosX = clib["getDataPointPosX"]
        self.getDataPointPosX.argtypes = (c_float, c_float, c_float, c_int, c_int)
        self.getDataPointPosX.restype = c_float
        
        self.getDataPointPosY = clib["getDataPointPosY"]
        self.getDataPointPosY.argtypes = (c_float, c_float, c_float, c_float, c_float, c_int, c_float)
        self.getDataPointPosY.restype = c_float


    def updateGraph(self, data, key, xLabel, index, left=50.0, right=10.0, top=10.0, bottom=20.0):
        self.canvas.delete("all")

        # x축, y축 그리기
        self.canvas.create_line(left, self.height-bottom, self.width-right, self.height-bottom)
        self.canvas.create_line(left, top, left, self.height - bottom)

        xAxis, yAxis, values = extractFromData(data, key, xLabel, 5, 4)

        # x축 칸 그리기
        nx = len(xAxis)
        for i in range(nx):
            self.canvas.create_line(left + (self.width - left - right) / (nx * 2) + i * (self.width - left - right) / nx,
                                    self.height - bottom - 5,
                                    left + (self.width - left - right) / (nx * 2) + i * (self.width - left - right) / nx,
                                    self.height - bottom + 5)

        # y축 칸 그리기
        ny = len(yAxis)
        for i in range(ny):
            self.canvas.create_line(left - 5,
                                    top + (self.height - top - bottom) / (ny * 2) + i * (self.height - top - bottom) / ny,
                                    left + 5,
                                    top + (self.height - top - bottom) / (ny * 2) + i * (self.height - top - bottom) / ny)

        # x축 칸 텍스트 그리기
        for i in range(nx):
            self.canvas.create_text(left + (self.width - left - right) / (nx * 2) + i * (self.width - left - right) / nx,
                                    self.height - bottom + (bottom / 2),
                                    text=str(xAxis[i]))

        # y축 칸 텍스트 그리기
        for i in range(ny):
            self.canvas.create_text(left - (left / 2),
                                    top + (self.height - top - bottom) / (ny * 2) + i * (self.height - top - bottom) / ny,
                                    text=str(yAxis[i]))

        # 데이터 포인트 그리기
        n = len(values)
        for i in range(n):
            x = self.getDataPointPosX(self.width, left, right, nx, i)
            y = self.getDataPointPosY(self.height, top, bottom, max(values), min(values), ny, values[i])
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")

        # 데이터 라인 그리기
        for i in range(1, n):
            prev_x = self.getDataPointPosX(self.width, left, right, nx, i - 1)
            prev_y = self.getDataPointPosY(self.height, top, bottom, max(values), min(values), ny, values[i - 1])
            curr_x = self.getDataPointPosX(self.width, left, right, nx, i - 0)
            curr_y = self.getDataPointPosY(self.height, top, bottom, max(values), min(values), ny, values[i - 0])
            self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill="red")
                

        self.canvas.update()