from bs4 import BeautifulSoup
from news import News
from newsMail import *
import requests, urllib
import pandas as pd
import matplotlib.pyplot as plt
import os
base_url = "https://news.google.com"

# 구글 검색시스템을 이용하여 키워드와 관련있는 기사 크롤링
def google_news_clipping(keyword_input, limit=10):
    keyword = urllib.parse.quote(keyword_input)
    url = base_url + "/search?q=" + keyword + "&hl=ko&gl=KR&ceid=KR%3Ako"

    resp = requests.get(url)
    html_src = resp.text
    soup = BeautifulSoup(html_src, 'lxml')

    news_items = soup.select('div[class="xrnccd"]')

    links = []
    titles = []
    contents = []
    agencies = []
    reporting_dates = []
    reporting_times = []

    for item in news_items[:limit]:
        link = item.find('a', attrs={'class': 'VDXfz'}).get('href')
        news_link = base_url + link[1:]
        links.append(news_link)

        news_title = item.find('a', attrs={'class': 'DY5T1d'}).getText()
        titles.append(news_title)

        news_content = item.find('span', attrs={'class': 'xBbh9'}).text
        contents.append(news_content)

        news_agency = item.find('a', attrs={'class': 'wEwyrc AVN2gc uQIVzc Sksgp'}).text
        agencies.append(news_agency)

        news_reporting = item.find('time', attrs={'class': 'WW6dff uQIVzc Sksgp'})
        if news_reporting == None:
            reporting_dates.append("None")
            reporting_times.append("None")
        else:
            news_reporting_datetime = news_reporting.get('datetime').split('T')
            news_reporting_date = news_reporting_datetime[0]
            news_reporting_time = news_reporting_datetime[1][:-1]
            reporting_dates.append(news_reporting_date)
            reporting_times.append(news_reporting_time)

    result = {'link': links, 'title': titles, 'contents': contents, 'agency': agencies, 'date': reporting_dates,\
              'time': reporting_times}
    return result
# 뉴스 객체 생성
def create_google_news(keyword_input):
    limit = int(input("검색할 뉴스 개수를 입력하세요 : "))
    # 뉴스 데이터 딕셔너리
    news_dict = google_news_clipping(keyword_input, limit)
    # 뉴스 객체 저장 리스트
    news_items = []
    # 뉴스 객체 생성
    for i in range(len(news_dict['title'])):
        news_item = News(news_dict['title'][i], news_dict['link'][i], news_dict['contents'][i], news_dict['agency'][i], news_dict['date'][i], news_dict['time'][i])
        news_items.append(news_item)
    # 크롤링한 기사 출력
    for news_item in news_items:
        news_item.print()
    return news_items
# 날짜 별 뉴스 수 시각화
def googleNewsTrend(news_items, keyword_input):
    # 날짜별 뉴스 업로드 수 딕셔너리
    date_dict = {}
    for news_item in news_items:
        # 뉴스 기사 업로드 날짜
        date = news_item.date
        # 날짜를 알 수 없는 뉴스는 패스
        if date == "None":
            continue
        if date in date_dict:
            date_dict[date][0] += 1
        else:
            date_dict[date] = [1]

    # 날짜 순으로 정렬한 딕셔너리 만들기
    s_date_dict = {}
    for key in sorted(date_dict):
        s_date_dict[key] = date_dict[key]

    # matplotlib 한글폰트 오류 해결
    from matplotlib import font_manager, rc
    cwd = os.getcwd()
    font_path = os.path.join(cwd, "data", "malgun.ttf")
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    # 행은 딕셔너리의 key(날짜)로 지정
    # 열은 'count'로 지정 후 내용은 딕셔너리의 value(기사 작성된 수)로 채우기
    data = pd.DataFrame(s_date_dict.values(), index=s_date_dict.keys(), columns=[keyword_input+"'s news count"])
    # 데이터 출력
    #print(data, "\n")

    # 그래프 그리기
    data.plot()

    # 데이터 저장
    cwd = os.getcwd()
    data.to_csv(cwd+"/output/GoogleNews_{}.csv".format_map(keyword_input))
    # 그래프 저장
    output_filepath = os.path.join(cwd, "output", "google_news_graph.png")
    plt.savefig(output_filepath, dpi=300)
    plt.show()

def sendGoolgeNewsByGmail(news_items):
    news_num = input("몇개의 뉴스를 메일로 받고싶으신가요? : ")
    news_num = int(news_num)
    sendNewsByGmail(news_items[:news_num], "구글 뉴스 크롤링")

if __name__ == "__main__":
    keyword_input = input("검색어를 입력하세요 : ")
    news_items = create_google_news(keyword_input) # 뉴스객체 리스트 생성
    sendGoolgeNewsByGmail(news_items) # 크롤링한 뉴스 객체 메일로 보내기
    #googleNewsTrend(news_items, keyword_input) # 뉴스 업로드 횟수 시각화
