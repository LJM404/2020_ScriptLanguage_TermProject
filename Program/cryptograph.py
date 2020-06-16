key = b"**********"
iv = b"**********"

# 암호화된 파일의 내용을 복호화하는 함수.
# 복호화에 성공할 경우 Context를 반환, 실패할 경우 None을 반환
def decryptFileContext(module, filename):
    print("debug message: filename - ", filename)
    try:
        f = open(filename, "rb")
        buf = f.read()
        f.close()
    except:
        print("error message: failed to open", filename)
        return None

    # C모듈을 통해 복호화를 진행
    module.setupAESCBCMode(buf, key, iv)
    context = module.decryptBufAESCBCMode()
    module.clearAESCBCMode()

    # byte형식을 string형식으로 변환
    context = context.decode("UTF-8")
    return context