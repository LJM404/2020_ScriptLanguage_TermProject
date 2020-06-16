import json
from tkinter import filedialog


# 파일 읽기/쓰기 함수의 상태 반환 값
FILE_CANCEL, FILE_SUCCESS, FILE_FAILED = range(3)


# 데이터로 부터 파일 이름을 생성하는 함수
# 생성된 파일 이름을 반환한다.
def createFilename(data):
    filename = ""
    filename += data[len(data) - 1]["date"] + "_"
    filename += data[len(data) - 1]["time"][:2] +"h_"
    filename += data[len(data) - 1]["city"] + "_"
    filename += data[len(data) - 1]["station"]
    return filename


# json 파일에 데이터를 저장하는 함수
# 저장에 성공할 경우 FILE_SUCCESS를 반환, 취소할 경우 FILE_CANCEL을 반환, 실패할 경우 FILE_FAILED를 반환
def saveData(data, defaultFilename=""):
    filename = filedialog.asksaveasfilename(initialdir="./Data/files", initialfile=defaultFilename, title="저장하기", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    print("debug message: filename -",type(filename), filename)

    if filename == "":
        return FILE_CANCEL
    
    try:
        f = open(filename + ".json", 'w', encoding="UTF-8")
        f.write(json.dumps(data, indent=4))
        f.close()
    except:
        print("error message: file save failed.")
        return FILE_FAILED
    return FILE_SUCCESS


# json 파일에 있는 데이터를 불러오는 함수
# 불러오기에 성공할 경우 내용을 반환, 취소할 경우 FILE_CANCEL을 반환, 실패할 경우 FILE_FAILED를 반환
def loadData():
    filename = filedialog.askopenfilename(initialdir="./Data/files", title="불러오기", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    print("debug message: filename -",type(filename), filename)

    if filename == "":
        return FILE_CANCEL
    
    try:
        f = open(filename, 'r')
        context = json.loads(f.read())
        f.close()
    except:
        print("error message: file load failed.")
        return FILE_FAILED
    return context