import smtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from cryptograph import *


err_EMAIL_DECRYPT_FAILED = 0
err_EMAIL_SEND_FAILED = 1
EMAIL_SUCCESS = 2


# HTML Table을 생성하는 함수
# 생성된 HTML텍스트를 반환한다.
def buildHtmlTable(data):
    lastDate =data[len(data) - 1]["date"]
    city     =data[len(data) - 1]["city"]
    station  =data[len(data) - 1]["station"]

    time_0 = data[0]["time"]
    time_1 = data[1]["time"]
    time_2 = data[2]["time"]
    time_3 = data[3]["time"]
    time_4 = data[4]["time"]

    so2_0 = data[0]["so2"]
    so2_1 = data[1]["so2"]
    so2_2 = data[2]["so2"]
    so2_3 = data[3]["so2"]
    so2_4 = data[4]["so2"]

    co_0 = data[0]["co"]
    co_1 = data[1]["co"]
    co_2 = data[2]["co"]
    co_3 = data[3]["co"]
    co_4 = data[4]["co"]

    o3_0 = data[0]["o3"]
    o3_1 = data[1]["o3"]
    o3_2 = data[2]["o3"]
    o3_3 = data[3]["o3"]
    o3_4 = data[4]["o3"]

    no2_0 = data[0]["no2"]
    no2_1 = data[1]["no2"]
    no2_2 = data[2]["no2"]
    no2_3 = data[3]["no2"]
    no2_4 = data[4]["no2"]

    pm10_0 = data[0]["pm10"]
    pm10_1 = data[1]["pm10"]
    pm10_2 = data[2]["pm10"]
    pm10_3 = data[3]["pm10"]
    pm10_4 = data[4]["pm10"]

    pm25_0 = data[0]["pm25"]
    pm25_1 = data[1]["pm25"]
    pm25_2 = data[2]["pm25"]
    pm25_3 = data[3]["pm25"]
    pm25_4 = data[4]["pm25"]

    khai_0 = data[0]["khai"]
    khai_1 = data[1]["khai"]
    khai_2 = data[2]["khai"]
    khai_3 = data[3]["khai"]
    khai_4 = data[4]["khai"]

    HTML_FORMAT = f"""
    <html>
        <header>
            <meta charset="UTF-8">
            <title>대기환경정보</title>
        </header>
        <body>
            <table border="1" bordercolor="black" align="center">
                <tr align="center">
                    <p><td colspan="6">{lastDate} {city} {station} 대기정보</td>
                </tr>
                <tr align="center">
                    <th></th>
                    <th>{time_0}</th>
                    <th>{time_1}</th>
                    <th>{time_2}</th>
                    <th>{time_3}</th>
                    <th>{time_4}</th>    
                </tr>
                <tr align="center">
                    <td>아황산가스</td>
                    <td>{so2_0}</td>
                    <td>{so2_1}</td>
                    <td>{so2_2}</td>
                    <td>{so2_3}</td>
                    <td>{so2_4}</td>
                </tr>
                <tr align="center">
                    <td>일산화탄소</td>
                    <td>{co_0}</td>
                    <td>{co_1}</td>
                    <td>{co_2}</td>
                    <td>{co_3}</td>
                    <td>{co_4}</td>
                </tr>
                <tr align="center">
                    <td>오존</td>
                    <td>{o3_0}</td>
                    <td>{o3_1}</td>
                    <td>{o3_2}</td>
                    <td>{o3_3}</td>
                    <td>{o3_4}</td>
                </tr>
                <tr align="center">
                    <td>이산화질소</td>
                    <td>{no2_0}</td>
                    <td>{no2_1}</td>
                    <td>{no2_2}</td>
                    <td>{no2_3}</td>
                    <td>{no2_4}</td>
                </tr>
                <tr align="center">
                    <td>미세먼지(PM10)</td>
                    <td>{pm10_0}</td>
                    <td>{pm10_1}</td>
                    <td>{pm10_2}</td>
                    <td>{pm10_3}</td>
                    <td>{pm10_4}</td>
                </tr>
                <tr align="center">
                    <td>초미세먼지(PM2.5)</td>
                    <td>{pm25_0}</td>
                    <td>{pm25_1}</td>
                    <td>{pm25_2}</td>
                    <td>{pm25_3}</td>
                    <td>{pm25_4}</td>
                </tr>
                <tr align="center">
                    <td>통합대기환경수치</td>
                    <td>{khai_0}</td>
                    <td>{khai_1}</td>
                    <td>{khai_2}</td>
                    <td>{khai_3}</td>
                    <td>{khai_4}</td>
                </tr>
            </table>
        </body>
    </html>
    """
    return HTML_FORMAT


# HTML테이블로 정리된 데이터가 담긴 이메일을 전송하는 함수
# 이메일 전송에 성공할 경우 EMAIL_SUCCESS를 반환. 그 이외는 다음과 같다.
# err_EMAIL_DECRYPT_FAILED: 암호화된 파일 열기에 실패한 경우 
# err_EMAIL_SEND_FAILED: 이메일 보내기에 실패한 경우
def sendEmail(module, data, id, server):
    htmlText = buildHtmlTable(data)
    print("debug message:", htmlText)

    # SMTP 서버의 주소와 포트 번호
    host = "smtp.gmail.com"
    port = 587

    # 받는 사람의 이메일
    recipientAddr = id + "@" + server

    # 보내는 사람의 이메일과 비밀번호
    senderAddr = decryptFileContext(module, "./Data/resource/serviceEmailID.bin")
    senderPW = decryptFileContext(module, "./Data/resource/serviceEmailPW.bin")
    if (senderAddr is None) or (senderPW is None):
        return err_EMAIL_DECRYPT_FAILED

    msg = MIMEBase("multipart", "mixed")
    msg["Subject"] = "\"거기 공기 어때?\"에서 요청한 대기오염측정정보입니다."
    msg["From"] = senderAddr
    msg["To"] = recipientAddr

    htmlPart = MIMEText(htmlText, "html", "UTF-8")
    msg.attach(htmlPart)

    try:
        smtp = smtplib.SMTP(host=host, port=port)
        smtp.starttls()
        smtp.login(senderAddr, senderPW)
        smtp.sendmail(senderAddr, [recipientAddr], msg.as_string())
        smtp.close()
    except:
        print("error message: Email sending failed")
        return err_EMAIL_SEND_FAILED
    return EMAIL_SUCCESS