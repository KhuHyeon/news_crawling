import smtplib
from email.mime.text import MIMEText

def sendNewsByGmail(news_items,subject="NoTitle"):
    # "dlgustjd1687@naver.com"
    recipients = input("받을 사람의 이메일을 입력해주세요 : ")
    # SMTP 서버 접속
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.ehlo()
    smtp_server.starttls()
    # Gmail server login
    my_addr = 'hong867103120@gmail.com'
    my_pw = 'dovftlheucluhbdj'
    smtp_server.login(user=my_addr, password=my_pw)
    # 보낼 내용
    body = ""
    # 구분선
    line = '\n' + '-' * 160 + '\n'
    # 메일로 보낸 뉴스 갯수
    index = 1
    for news_item in news_items:
        body += ("{}번째 뉴스\n제목 : {}\n링크 : {}\n내용 : {}\n언론사 : {}\n날짜&시간 : {}"
                 .format(index, news_item.title, news_item.link, news_item.contents, news_item.agency, news_item.date + " " + news_item.time + line))
        index += 1
    my_msg = MIMEText(body)
    my_msg['Subject'] = subject
    my_msg['To'] = recipients

    # 이메일 발송
    smtp_server.sendmail(from_addr=my_addr, to_addrs=recipients, msg=my_msg.as_string())
    smtp_server.quit()
    print("{}님에게 이메일을 발송하였습니다.".format(recipients))