import json
from tkinter import filedialog

# 파일 읽기/쓰기 함수의 상태 반환 값
FILE_CANCEL, FILE_SUCCESS, FILE_FAILED = range(3)

# json 파일에 데이터를 저장하는 함수
def saveData(data, defaultFilename=""):
    filename = filedialog.asksaveasfilename(initialdir="./Data/files", initialfile=defaultFilename, title="저장하기", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    print("debug message: filename -",type(filename), filename)

    if filename == "":
        return FILE_CANCEL
        
    f = open(filename + ".json", 'w', encoding="UTF-8")
    f.write(json.dumps(data, indent=4))
    f.close()
    return FILE_SUCCESS


# json 파일에 있는 데이터를 읽는 함수
def loadData():
    filename = filedialog.askopenfilename(initialdir="./Data/files", title="불러오기", filetypes=(("json files", "*.json"), ("all files", "*.*")))
    print("debug message: filename -",type(filename), filename)

    if filename == "":
        return FILE_CANCEL, None
    
    try:
        f = open(filename, 'r')
        context = json.loads(f.read())
        print("debug message", type(context), context)
        f.close()
    except json.JSONDecodeError as err:
        print("debug message:", err)
        return FILE_FAILED, None
    return FILE_SUCCESS, context