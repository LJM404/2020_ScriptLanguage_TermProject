from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from graphBox import GraphBox
from service import *
from names import *


class Program:
    def __init__(self):
        self.window = Tk()
        self.window.title("거기 공기 어때?")
        self.window.geometry("750x300") # 종횡비( 2.5:1 )
        self.window.resizable(False, False)
        self.setupProgram()

        self.programData = None

        self.window.mainloop()


    def setupProgram(self):
        # 왼쪽 프레임
        self.leftFrame = ttk.LabelFrame(self.window, text="대기오염정보")
        self.leftFrame.place(x=20, y=10, width=350, height=270)

        # 오른쪽 프레임
        self.rightFrame = ttk.LabelFrame(self.window, text="그래프")
        self.rightFrame.place(x=380, y=10, width=350, height=270)

        # 측정정보 프레임
        self.infoFrame = ttk.LabelFrame(self.leftFrame, text="측정정보")
        self.infoFrame.place(x=15, y=30, width=205, height=180)

        # 상태 이미지 프레임
        self.imageFrame = ttk.LabelFrame(self.leftFrame, text="대기오염상태")
        self.imageFrame.place(x=235, y=30, width=95, height=180)

        # 그래프박스
        self.graphbox = GraphBox(self.rightFrame, x=5, y=0, width=330, height=210)
        self.graphbox.updateGraph(None, None, None, None)

        # 검색 버튼
        self.searchButton = ttk.Button(self.leftFrame, text="검색", width=12, command=self.pressedSearchButton)
        self.searchButton["state"] = "disabled"
        self.searchButton.place(x=235, y=0)

        # 도시 콤보박스
        self.cityStr = StringVar()
        self.cityCombobox = ttk.Combobox(self.leftFrame, width=10, values=list(sidoNames.keys()), textvariable=self.cityStr, state="readonly")
        self.cityCombobox.current(0)
        self.cityCombobox.place(x=15, y=1)

        # 측정소 콤보박스
        self.stationStr = StringVar()
        self.stationCombobox = ttk.Combobox(self.leftFrame, width=10, values=list(stationNames[self.cityStr.get()].keys()), textvariable=self.stationStr, state="readonly")
        self.stationCombobox.current(0)
        self.stationCombobox.place(x=125, y=1)

        # 도시 - 측정소 업데이트 함수 설정
        self.cityStr.trace('w', self.updateCityStr)
        self.stationStr.trace('w', self.updateStationStr)

        # 보내기 버튼
        self.sendButton = ttk.Button(self.leftFrame, text="보내기", width=12, command=self.pressedSendButton)
        self.sendButton["state"] = "disabled"
        self.sendButton.place(x=235, y=220)

        # 이메일 아이디 입력 엔트리
        self.emailIDStr = StringVar()
        self.emailIDStr.set("이메일 아이디")
        self.emailIDEntry = ttk.Entry(self.leftFrame, width=12, textvariable=self.emailIDStr)
        self.emailIDEntry.place(x=15, y=221)

        # 이메일 서버 입력 콤보박스
        self.emailServerStr = StringVar()
        self.emailServerCombobox = ttk.Combobox(self.leftFrame, width=10, values=serverNames, textvariable=self.emailServerStr)
        self.emailServerCombobox.current(0)
        self.emailServerCombobox.place(x=125, y=221)

        # 이메일 아이디 - 서버 업데이트 함수 설정
        self.emailIDStr.trace('w', self.updateEmailIDStr)
        self.emailServerStr.trace('w', self.updateEmailServerStr)
        self.emailIDEntry.bind("<FocusIn>", self.updateEmailIDEntry)
        self.emailIDEntry.bind("<FocusOut>", self.updateEmailIDEntry)
        self.emailServerCombobox.bind("<FocusIn>", self.updateEmailServerCombobox)
        self.emailServerCombobox.bind("<FocusOut>", self.updateEmailServerCombobox)
        
        # 그래프 콤보박스
        self.graphStr = StringVar()
        self.graphCombobox = ttk.Combobox(self.rightFrame, width=15, values=list(dataList.keys()), textvariable=self.graphStr, state="readonly")
        self.graphCombobox.current(0)
        self.graphCombobox.place(x=10, y=221)

        # 그래프 콤보박스 업데이트 함수 설정
        self.graphStr.trace('w', self.updateGraphStr)

        # 저장 버튼
        self.saveButton = ttk.Button(self.rightFrame, text="저장", width=10, command=self.pressedSaveButton)
        self.saveButton["state"] = "disabled"
        self.saveButton.place(x=170, y=220)

        # 불러오기 버튼
        self.loadButton = ttk.Button(self.rightFrame, text="불러오기", width=10, command=self.pressedLoadButton)
        self.loadButton.place(x=255, y=220)

        # 상태 이미지 라벨
        p = PhotoImage(file="./Data/" + imageNames["없음"])
        self.imageLabel = ttk.Label(self.imageFrame, image=p)
        self.imageLabel.image = p
        self.imageLabel.place(x=1, y=0)

        # 측정정보라벨들
        self.cityLabel = ttk.Label(self.infoFrame, text="도시:")
        self.cityLabel.place(x=10, y=0)
        self.stationLabel = ttk.Label(self.infoFrame, text="측정소:")
        self.stationLabel.place(x=10, y=15)
        self.dateLabel = ttk.Label(self.infoFrame, text="측정일자:")
        self.dateLabel.place(x=10, y=30)
        self.so2Label = ttk.Label(self.infoFrame, text="아황산가스 농도:")
        self.so2Label.place(x=10, y=45)
        self.coLabel = ttk.Label(self.infoFrame, text="일산화탄소 농도:")
        self.coLabel.place(x=10, y=60)
        self.o3Label = ttk.Label(self.infoFrame, text="오존 농도:")
        self.o3Label.place(x=10, y=75)
        self.no2Label = ttk.Label(self.infoFrame, text="이산화질소 농도:")
        self.no2Label.place(x=10, y=90)
        self.pm10Label = ttk.Label(self.infoFrame, text="미세먼지(PM10) 농도:")
        self.pm10Label.place(x=10, y=105)
        self.pm25Label = ttk.Label(self.infoFrame, text="미세먼지(PM2.5) 농도:")
        self.pm25Label.place(x=10, y=120)
        self.khaiLabel = ttk.Label(self.infoFrame, text="통합대기환경수치:")
        self.khaiLabel.place(x=10, y=135)


    def pressedSearchButton(self):
        print("debug message: pressed search button")
        self.programData = getMsrstnAcctoRltmMesureDnsty(sido=self.cityStr.get(), station=self.stationStr.get())
        self.graphbox.updateGraph(self.programData, dataList[self.graphStr.get()], "time", 0)
        self.updateInfoLabels(len(self.programData) - 1)
        self.updateImageLabel(self.programData[len(self.programData) - 1]["khai"])


    def pressedSendButton(self):
        print("debug message: pressed send button")

    
    def pressedSaveButton(self):
        print("debug message: pressed save button")


    def pressedLoadButton(self):
        print("debug message: pressed load button")


    def updateCityStr(self, index, value, op):
        print("debug message: update city string var")
        self.stationCombobox["values"] = list(stationNames[self.cityStr.get()].keys())
        self.stationCombobox.current(0)


    def updateStationStr(self, index, value, op):
        print("debug message: update station string var")
        if self.stationStr.get() == "측정소": self.searchButton["state"] = "disabled"
        else: self.searchButton["state"] = "active"


    def updateEmailIDStr(self, index, value, op):
        print("debug message: update email id string var")
        if (self.emailIDStr.get() != "") and (self.emailIDStr.get() != "이메일 아이디") and (self.emailServerStr.get() != "") and (self.emailServerStr.get() != "이메일 주소"): self.sendButton["state"] = "active"
        else: self.sendButton["state"] = "disabled"


    def updateEmailServerStr(self, index, value, op):
        print("debug message: update email server string var")
        if (self.emailIDStr.get() != "") and (self.emailIDStr.get() != "이메일 아이디") and (self.emailServerStr.get() != "") and (self.emailServerStr.get() != "이메일 주소"): self.sendButton["state"] = "active"
        else: self.sendButton["state"] = "disabled"

    
    def updateEmailIDEntry(self, event):
        print("debug message: update Email id entry")
        if self.emailIDStr.get() == "이메일 아이디": self.emailIDStr.set("")
        elif self.emailIDStr.get() == "": self.emailIDStr.set("이메일 아이디")


    def updateEmailServerCombobox(self, event):
        print("debug message: update Email server combobox")
        if self.emailServerStr.get() == "이메일 주소": self.emailServerStr.set("")
        elif self.emailServerStr.get() == "": self.emailServerStr.set("이메일 주소")


    def updateGraphStr(self, index, value, op):
        print("debug message: update Graph string var")
        self.graphbox.updateGraph(self.programData, dataList[self.graphStr.get()], "time", 0)


    def updateInfoLabels(self, index):
        if self.programData is not None:
            self.cityLabel.configure(text="도시: " + str(self.programData[index]["city"]))
            self.stationLabel.configure(text="측정소: " + str(self.programData[index]["station"]))
            self.dateLabel.configure(text="측정일자: " + str(self.programData[index]["date"]) + " " + str(self.programData[index]["time"]))
            self.so2Label.configure(text="아황산가스 농도: " + str(self.programData[index]["so2"]))
            self.coLabel.configure(text="일산화탄소 농도: " + str(self.programData[index]["co"]))
            self.o3Label.configure(text="오존 농도: " + str(self.programData[index]["o3"]))
            self.no2Label.configure(text="이산화질소 농도: " + str(self.programData[index]["no2"]))
            self.pm10Label.configure(text="미세먼지(PM10) 농도: " + str(self.programData[index]["pm10"]))
            self.pm25Label.configure(text="미세먼지(PM2.5) 농도: " + str(self.programData[index]["pm25"]))
            self.khaiLabel.configure(text="통합대기환경수치: " + str(self.programData[index]["khai"]))
        else:
            self.cityLabel.configure(text="도시: ")
            self.stationLabel.configure(text="측정소: ")
            self.dateLabel.configure(text="측정일자: ")
            self.so2Label.configure(text="아황산가스 농도: ")
            self.coLabel.configure(text="일산화탄소 농도: ")
            self.o3Label.configure(text="오존 농도: ")
            self.no2Label.configure(text="이산화질소 농도: ")
            self.pm10Label.configure(text="미세먼지(PM10) 농도: ")
            self.pm25Label.configure(text="미세먼지(PM2.5) 농도: ")
            self.khaiLabel.configure(text="통합대기환경수치: ")


    def updateImageLabel(self, value):
        if value is None:
            p = PhotoImage(file="./Data/" + imageNames["없음"])
        elif (0 <= value) and (value <= 50):
            p = PhotoImage(file="./Data/" + imageNames["좋음"])
        elif (51 <= value) and (value <= 100):
            p = PhotoImage(file="./Data/" + imageNames["보통"])
        elif (101 <= value) and (value <= 250):
            p = PhotoImage(file="./Data/" + imageNames["나쁨"])
        elif (251 <= value):
            p = PhotoImage(file="./Data/" + imageNames["심각"])
        self.imageLabel.configure(image=p)
        self.imageLabel.image = p