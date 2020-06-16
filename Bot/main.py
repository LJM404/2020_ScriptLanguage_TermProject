import telepot
from telepot.loop import MessageLoop
from service import *
from module import *


def getBotToken():
    f = open("./Data/resource/BotToken.bin", "rb")
    module = CModule()
    module.setupAESCBCMode(f.read(), b"**********", b"**********")
    token = module.decryptBufAESCBCMode()
    module.clearAESCBCMode()
    token = token.decode("UTF-8")
    f.close()
    print("bot token:", token)
    return token


# 도움말을 보내는 함수
def replyHelp(chatID):
    msg = "대기오염상태 봇 사용법\n"
    msg += "\h - 대기오염 상태 봇의 사용방법을 알려줍니다.\n"
    msg += "\s [도시] [측정소] - 선택한 도시의 측정소에서 측정된 최근의 대기오염상태를 알려줍니다.\n"
    bot.sendMessage(chatID, msg)


# 선택한 도시와 측정소에서 최근의 측정된 대기오염상태를 보내는 함수 
def replySearch(chatID, sido, station):
    msg = ""
    if (sido in sidoNames.keys()) and (station in stationNames[sido].keys()):
        data = getMsrstnAcctoRltmMesureDnsty(sido, station, 1)
        if data is not None:
            msg += "최근의 대기오염상태 측정 결과\n"
            msg += "도시: {0}\n".format(data[0]["city"])
            msg += "측정소: {0}\n".format(data[0]["station"])
            msg += "측정일자: {0} {1}\n".format(data[0]["date"], data[0]["time"])
            msg += "아황산가스농도: {0}\n".format(data[0]["so2"])
            msg += "일산화탄소농도: {0}\n".format(data[0]["co"])
            msg += "오존농도: {0}\n".format(data[0]["o3"])
            msg += "이산화질소농도: {0}\n".format(data[0]["no2"])
            msg += "미세먼지(PM10)농도: {0}\n".format(data[0]["pm10"])
            msg += "초미세먼지(PM2.5)농도: {0}\n".format(data[0]["pm25"])
            msg += "통합대기환경수치: {0}\n".format(data[0]["khai"])
        else:
            msg += "죄송합니다. 대기오염상태를 검색하지 못했습니다.\n 잠시 후 다시 시도해 주세요.\n"
    else:
        msg += "도시와 측정소의 이름을 정확히 입력해 주세요.\n"
    bot.sendMessage(chatID, msg)


# 봇의 메세지 처리 함수
def msgHandler(msg):
    print("listen message:", msg)
    print('-'*64)

    contentType, chatType, chatID = telepot.glance(msg)
    if contentType == "text":
        text = msg["text"]
        args = text.split(' ')
        if ((args[0] == "/도움말") or (args[0] == "/h")) and (len(args) >= 1): 
            replyHelp(chatID)
            return
        elif ((args[0] == "/검색") or (args[0] == "/s")) and (len(args) >= 3):
            replySearch(chatID, args[1], args[2])
            return
    replyHelp(chatID)


# 프로그램 진입점
TOKEN = getBotToken()
bot = telepot.Bot(TOKEN)

print("Start Bot Service...")
MessageLoop(bot, msgHandler).run_as_thread()

while True:
    s = input()
    if (s == 'q') or (s == 'Q'):
        break 
print("Bot Service Termination...")