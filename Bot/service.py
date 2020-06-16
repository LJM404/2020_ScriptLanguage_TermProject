from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from names import *

SERVICE_URL = 'http://openapi.airkorea.or.kr/openapi/services/rest'
SERVICE_NAME = 'ArpltnInforInqireSvc'
SERVICE_KEY = 'EM5flydqDY%2F%2B9QgXDcBu0tgVqAc941So9w7OcuFP%2Bpr5WtNNZ%2BCmAVAbo8%2Bs4VVMuuo9wDYhItuZ8BY6kpxC%2Bg%3D%3D'

# URL을 만들어주는 함수
def urlBuilder(serviceOperation, **options):
    s = SERVICE_URL + '/' + SERVICE_NAME + '/' + serviceOperation + "?serviceKey=" + SERVICE_KEY
    for key in options.keys():
        s += '&' + key + '=' + str(options[key])
    return s

# 측정소별 실시간 측정정보 조회
def getMsrstnAcctoRltmMesureDnsty(sido, station, numOfRows=5, pageNo=1, dataTerm="DAILY", ver=1.3):
    url = urlBuilder("getMsrstnAcctoRltmMesureDnsty", numOfRows=numOfRows, pageNo=pageNo, stationName=stationNames[sido][station], dataTerm=dataTerm, ver=ver)
    print(url)
    
    try:
        html = urlopen(url)
    except URLError as e:
        print("error message:", e)
        return None

    try:
        soup = BeautifulSoup(html, "html.parser")

        totalCount = soup.find("totalcount")    # 쿼리한 데이터의 총 갯수
        times = soup.find_all("datatime")       # 측정 시간들
        so2Values = soup.find_all("so2value")   # 아황산가스 농도
        coValues = soup.find_all("covalue")     # 일산화탄소 농도
        o3Values = soup.find_all("o3value")     # 오존 농도
        no2Values = soup.find_all("no2value")   # 이산화질소 농도
        pm10Values = soup.find_all("pm10value") # 미세먼지(PM10) 농도
        pm25Values = soup.find_all("pm25value") # 미세먼지(PM2.5) 농도
        khaiValues = soup.find_all("khaivalue") # 통합대기환경수치
    except AttributeError as e:
        print("error message:", e)
        return None


    results = []
    for i in range(0, min(numOfRows, int(totalCount.string))):
        so2, co, o3, no2, pm10, pm25, khai = None, None, None, None, None, None, None
        
        if str(so2Values[i].string) != '-': so2=float(so2Values[i].string)
        if str(coValues[i].string) != '-': co=float(coValues[i].string)
        if str(o3Values[i].string) != '-': o3=float(o3Values[i].string)
        if str(no2Values[i].string) != '-': no2=float(no2Values[i].string)
        if str(pm10Values[i].string) != '-': pm10=float(pm10Values[i].string)
        if str(pm25Values[i].string) != '-': pm25=float(pm25Values[i].string)
        if str(khaiValues[i].string) != '-': khai=float(khaiValues[i].string)

        temp = {}
        temp.update(city=sido)
        temp.update(station=station)
        temp.update(date=str(times[i].string).split()[0])
        temp.update(time=str(times[i].string).split()[1])
        temp.update(so2=so2)
        temp.update(co=co)
        temp.update(o3=o3)
        temp.update(no2=no2)
        temp.update(pm10=pm10)
        temp.update(pm25=pm25)
        temp.update(khai=khai)

        results.insert(0, temp)
    return results