from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from graphBox import *
from service import *
from module import *
from names import *
from files import *
from mail import *


class Program:
    def __init__(self):
        self.window = Tk()
        self.window.title("거기 공기 어때?")
        self.window.geometry("750x300") # 종횡비( 2.5:1 )
        self.window.resizable(False, False)
        self.setupProgram()
        self.programData = None
        self.programDataIndex = 0
        self.window.mainloop()


    # 프로그램의 초기 설정을 하는 함수
    def setupProgram(self):
        # C/C++로 작성된 동적라이브러리 함수를 연결
        self.module = CModule()

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
        self.graphbox = GraphBox(self.rightFrame, self.module, x=5, y=0, width=330, height=210)
        self.graphbox.updateGraph(None, None, None, None)
        self.graphbox.bind("<ButtonRelease-1>", self.updateGraphbox)

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
        p = PhotoImage(file="./Data/resource/" + imageNames["없음"])
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


    # 검색 버튼 콜백 함수
    # OpenAPI를 이용하여 측정정보목록을 얻는다.
    def pressedSearchButton(self):
        print("debug message: pressed search button")
        result = getMsrstnAcctoRltmMesureDnsty(self.module, self.cityStr.get(), self.stationStr.get())
        if result == err_SERVICE_DECRYPT_FAILED:
            messagebox.showerror(title="검색 실패", message="서비스 키 생성에 실패했습니다.\n프로그램을 다시 설치해 주세요.")
        elif result == err_SERVICE_CONNECT_FAILED:
            messagebox.showerror(title="검색 실패", message="서비스 연결에 실패했습니다.\n네트워크 상태를 점검해 주세요.")
        elif result == err_SERVICE_PARSER_FAILED:
            messagebox.showerror(title="검색 실패", message="서비스 처리에 실패했습니다.\n프로그램 관리자에게 문의해 주세요.")
        else:
            self.updateProgramData(result)
    

    # 보내기 버튼 콜백 함수
    def pressedSendButton(self):
        print("debug message: pressed send button")
        result = sendEmail(self.module, self.programData, self.emailIDStr.get(), self.emailServerStr.get())
        if result == err_EMAIL_DECRYPT_FAILED:
            messagebox.showerror(title="이메일 전송 실패", message="이메일 서비스 생성에 실패했습니다.\n프로그램을 다시 설치해 주세요.")
        elif result == err_EMAIL_SEND_FAILED:
            messagebox.showerror(title="이메일 전송 실패", message="이메일 전송에 실패했습니다.\n네트워크 상태 또는 이메일 주소를 확인해 주세요.")
        else:
            messagebox.showinfo(title="이메일 전송 성공", message="이메일 전송에 성공했습니다.")

    
    # 저장하기 버튼 콜백 함수
    def pressedSaveButton(self):
        print("debug message: pressed save button")
        result = saveData(self.programData, createFilename(self.programData))
        if result == FILE_SUCCESS:
            messagebox.showinfo(title="저장하기 성공", message="파일을 저장했습니다.")
        elif result == FILE_FAILED:
            messagebox.showerror(title="저장하기 실패", message="파일 저장하기에 실패했습니다.")


    # 불러오기 버튼 콜백 함수
    def pressedLoadButton(self):
        print("debug message: pressed load button")
        result = loadData()
        if result == FILE_FAILED: 
            messagebox.showerror(title="불러오기 실패", message="파일 불러오기에 실패했습니다.")
        elif result != FILE_CANCEL: 
            self.updateProgramData(result)


    # cityStr 콜백 함수 - 도시 이름에 따라 측정소 콤보박스의 내용을 변경 한다.
    def updateCityStr(self, index, value, op):
        print("debug message: update city string var")
        self.stationCombobox["values"] = list(stationNames[self.cityStr.get()].keys())
        self.stationCombobox.current(0)


    # stationStr 콜백함수 - 검색 버튼 활성화를 결정한다.
    def updateStationStr(self, index, value, op):
        print("debug message: update station string var")
        if self.stationStr.get() == "측정소": self.searchButton["state"] = "disabled"
        else: self.searchButton["state"] = "active"


    # EmailIDStr 콜백함수 - 보내기 버튼 활성화를 결정한다.
    def updateEmailIDStr(self, index, value, op):
        print("debug message: update email id string var")
        if (self.emailIDStr.get() != "") and (self.emailIDStr.get() != "이메일 아이디") and (self.emailServerStr.get() != "") and (self.emailServerStr.get() != "이메일 주소") and (self.programData is not None) : self.sendButton["state"] = "active"
        else: self.sendButton["state"] = "disabled"


    # emailServerStr 콜백함수 - 보내기 버튼 활성화를 결정한다.
    def updateEmailServerStr(self, index, value, op):
        print("debug message: update email server string var")
        if (self.emailIDStr.get() != "") and (self.emailIDStr.get() != "이메일 아이디") and (self.emailServerStr.get() != "") and (self.emailServerStr.get() != "이메일 주소") and (self.programData is not None): self.sendButton["state"] = "active"
        else: self.sendButton["state"] = "disabled"

    
    # 이메일 아이디 입력창 콜백함수
    def updateEmailIDEntry(self, event):
        print("debug message: update Email id entry")
        if self.emailIDStr.get() == "이메일 아이디": self.emailIDStr.set("")
        elif self.emailIDStr.get() == "": self.emailIDStr.set("이메일 아이디")


    # 이메일 주소 입력창 콜백함수
    def updateEmailServerCombobox(self, event):
        print("debug message: update Email server combobox")
        if self.emailServerStr.get() == "이메일 주소": self.emailServerStr.set("")
        elif self.emailServerStr.get() == "": self.emailServerStr.set("이메일 주소")


    # graphStr 콜백함수 - 그래프박스의 그래프 내용을 업데이트한다.
    def updateGraphStr(self, index, value, op):
        print("debug message: update Graph string var")
        self.graphbox.updateGraph(self.programData, dataList[self.graphStr.get()], "time", self.programDataIndex)


    # 그래프 박스 콜백 함수 - 그래프박스의 마우스 입력을 처리한다.
    def updateGraphbox(self, event):
        print("debug message: update Graphbox")
        result = self.graphbox.checkGraphPoint(event.x, event.y, self.programData, dataList[self.graphStr.get()], "time")
        if result is not None:
            self.programDataIndex = result        
            self.graphbox.updateGraph(self.programData, dataList[self.graphStr.get()], "time", self.programDataIndex)
            self.updateInfoLabels(self.programData, self.programDataIndex)
            self.updateImageLabel(self.programData, self.programDataIndex)



    # programData를 업데이트 할 때 호출하는 함수
    # 새로운 데이터가 적합한지 확인하고 업데이트한다.
    def updateProgramData(self, newData):
        if self.checkProgramData(newData) == False:
            messagebox.showerror(title="데이터 오류", message="데이터가 손상되어 사용할 수 없습니다.")
            self.programData = None
            self.programDataIndex = 0
        else: 
            self.programData = newData
            self.programDataIndex = len(self.programData) - 1

        self.graphbox.updateGraph(self.programData, dataList[self.graphStr.get()], "time", self.programDataIndex)
        self.updateInfoLabels(self.programData, self.programDataIndex)
        self.updateImageLabel(self.programData, self.programDataIndex)
        
        if (self.emailIDStr.get() != "") and (self.emailIDStr.get() != "이메일 아이디") and (self.emailServerStr.get() != "") and (self.emailServerStr.get() != "이메일 주소") and (self.programData is not None) : 
            self.sendButton["state"] = "active"
        else:
            self.sendButton["state"] = "disabled"

        if (self.programData is not None): 
            self.saveButton["state"] = "active"
        else:
            self.saveButton["state"] = "disabled"


    # 측정정보 라벨들을 현재 가진 데이터로 업데이트 하는 함수
    def updateInfoLabels(self, data, index):
        if data is not None:
            self.cityLabel.configure(text="도시: " + str(data[index]["city"]))
            self.stationLabel.configure(text="측정소: " + str(data[index]["station"]))
            self.dateLabel.configure(text="측정일자: " + str(data[index]["date"]) + " " + str(data[index]["time"]))
            self.so2Label.configure(text="아황산가스 농도: " + str(data[index]["so2"]))
            self.coLabel.configure(text="일산화탄소 농도: " + str(data[index]["co"]))
            self.o3Label.configure(text="오존 농도: " + str(data[index]["o3"]))
            self.no2Label.configure(text="이산화질소 농도: " + str(data[index]["no2"]))
            self.pm10Label.configure(text="미세먼지(PM10) 농도: " + str(data[index]["pm10"]))
            self.pm25Label.configure(text="미세먼지(PM2.5) 농도: " + str(data[index]["pm25"]))
            self.khaiLabel.configure(text="통합대기환경수치: " + str(data[index]["khai"]))
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


    # 상태 이미지를 현재 가진 데이터의 통합대기환경수치에 따라 다른 상태 이미지로 업데이트 하는 함수
    def updateImageLabel(self, data, index):
        if (data is None) or (data[index]["khai"] is None):
            p = PhotoImage(file="./Data/resource/" + imageNames["없음"])
        elif (0 <= data[index]["khai"]) and (data[index]["khai"] <= 50):
            p = PhotoImage(file="./Data/resource/" + imageNames["좋음"])
        elif (51 <= data[index]["khai"]) and (data[index]["khai"] <= 100):
            p = PhotoImage(file="./Data/resource/" + imageNames["보통"])
        elif (101 <= data[index]["khai"]) and (data[index]["khai"] <= 250):
            p = PhotoImage(file="./Data/resource/" + imageNames["나쁨"])
        elif (251 <= data[index]["khai"]):
            p = PhotoImage(file="./Data/resource/" + imageNames["심각"])
        self.imageLabel.configure(image=p)
        self.imageLabel.image = p

    
    # 데이터가 프로그램에 사용하기 적합한지 확인하는 함수
    # 사용하기 적합한 경우 True를 반환한다.
    @staticmethod
    def checkProgramData(newData):
        if type(newData) is list:
            for data in newData:
                if ("city" in data) and ("station" in data) and ("date" in data) and ("time" in data) and ("so2" in data) and ("co" in data) and ("o3" in data) and ("no2" in data) and ("pm10" in data) and ("pm25" in data) and ("khai" in data):
                    continue
                else:
                    return False
            return True
        else:
            return False