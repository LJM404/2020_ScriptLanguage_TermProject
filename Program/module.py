from ctypes import *

# C로 작성된 동적라이브러리 함수와 연결한다.
class CModule:
    def __init__(self):
        clib = cdll.LoadLibrary("./Module/calcModule.dll")
        self.getDataPointPosX = clib["getDataPointPosX"]
        self.getDataPointPosX.argtypes = (c_float, c_float, c_float, c_int, c_int)
        self.getDataPointPosX.restype = c_float

        self.getDataPointPosY = clib["getDataPointPosY"]
        self.getDataPointPosY.argtypes = (c_float, c_float, c_float, c_float, c_float, c_int, c_float)
        self.getDataPointPosY.restype = c_float

        clib = cdll.LoadLibrary("./Module/cryptoModule.dll")
        self.setupAESCBCMode = clib["setupAESCBCMode"]
        self.setupAESCBCMode.argtypes = (c_char_p, c_char_p, c_char_p)
        self.setupAESCBCMode.restype = None

        self.clearAESCBCMode = clib["clearAESCBCMode"]
        self.clearAESCBCMode.argtypes = ()
        self.clearAESCBCMode.restype = None

        self.encryptBufAESCBCMode = clib["encryptBufAESCBCMode"]
        self.encryptBufAESCBCMode.argtypes = ()
        self.encryptBufAESCBCMode.restype = c_char_p

        self.decryptBufAESCBCMode = clib["decryptBufAESCBCMode"]
        self.decryptBufAESCBCMode.argtypes = ()
        self.decryptBufAESCBCMode.restype = c_char_p