from bs4 import BeautifulSoup
from selenium import webdriver
import requests

main_url = "https://news.naver.com/"
base_url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105#&date=%2000:00:00&page='

# 각각의 네이버 뉴스 페이지에 접근하여 뉴스 모든 기사 크롤링 하는 함수
def naver_news_clipping(limit=1):
    # data_list
    links = []
    titles = []
    contents = []
    agencies = []
    reporting_dates = []
    reporting_times = []

    # pagination 1~limit
    for page_num in range(1, limit + 1):
        url = base_url + str(page_num)

        # Selenium & BeautifulSoup
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        news_item = soup.select('div[class=section_body]')

        # find link
        for items in news_item:
            # title & link in tl_items
            tl_items = items.select('ul > li > dl > dt > a')
            for tl_item in tl_items:
                # add url to links list
                full_url = main_url + tl_item.get('href')
                if full_url in links:
                    continue
                links.append(full_url)

        # close the chrome's tab
        driver.close()
    # -- add all links in page to links list -- #

    # use links to go each news
    for link in links:
        resp = requests.get(link)
        html_src = resp.text
        soup = BeautifulSoup(html_src, 'html.parser')
        news_items = soup.select('div[class="content"]')

        # set data
        for item in news_items:
            # title
            title = soup.select_one('#articleTitle').text
            titles.append(title)

            # content
            content = soup.select_one('#articleBodyContents').text.strip()
            contents.append(content)
            # reporting_date & time
            reporting_dateTime = soup.select_one(
                '#main_content > div.article_header > div.article_info > div > span.t11').text.split()
            reporting_date = reporting_dateTime[0][:-1]
            reporting_time = " ".join(reporting_dateTime[1:])
            reporting_dates.append(reporting_date)
            reporting_times.append(reporting_time)
            # agency
            agency = soup.select_one('#main_content > div.article_header > div.press_logo > a > img').get('title')
            agencies.append(agency)

    result = {'link': links, 'title': titles, 'contents': contents, 'agency': agencies, 'date': reporting_dates, \
              'time': reporting_times}
    return result

# 각각의 네이버 뉴스 페이지에 접근하여 키워드 포함한 뉴스 기사 크롤링 하는 함수
def naver_news_clipping_keyword(keyword_input, limit=1):
    # data_list
    links = []
    titles = []
    contents = []
    agencies = []
    reporting_dates = []
    reporting_times = []

    # pagination 1~limit
    for page_num in range(1, limit + 1):
        url = base_url + str(page_num)

        # Selenium & BeautifulSoup
        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        news_item = soup.select('div[class=section_body]')

        # find link
        for items in news_item:
            # title & link in tl_items
            tl_items = items.select('ul > li > dl > dt > a')
            # Check if the keyword exists in title
            for tl_item in tl_items:
                title = tl_item.text
                if title != "":
                    if keyword_input in title:
                        # exists in title -> append
                        titles.append(title)
                    else:
                        # not exists in title -> skip
                        continue
                # add url to links list
                full_url = main_url + tl_item.get('href')
                if full_url in links:
                    continue
                links.append(full_url)
        # close the chrome's tab
        driver.close()
    # -- add all links in page to links list -- #

    # use links to go each news
    for link in links:
        resp = requests.get(link)
        html_src = resp.text
        soup = BeautifulSoup(html_src, 'html.parser')
        news_items = soup.select('div[class="content"]')

        # set data
        for item in news_items:
            '''
            # title
            title = soup.select_one('#articleTitle').text
            titles.append(title)
            '''
            # content
            content = soup.select_one('#articleBodyContents').text.strip()
            contents.append(content)
            # reporting_date & time
            reporting_dateTime = soup.select_one(
                '#main_content > div.article_header > div.article_info > div > span.t11').text.split()
            reporting_date = reporting_dateTime[0][:-1]
            reporting_time = " ".join(reporting_dateTime[1:])
            reporting_dates.append(reporting_date)
            reporting_times.append(reporting_time)
            # agency
            agency = soup.select_one('#main_content > div.article_header > div.press_logo > a > img').get('title')
            agencies.append(agency)

    result = {'link': links, 'title': titles, 'contents': contents, 'agency': agencies, 'date': reporting_dates, \
              'time': reporting_times}
    return result


search_word = input("검색어를 입력하세요 : ")
limit_page = int(input("검색할 페이지 범위를 입력하세요 : "))
#news_1 = naver_news_clipping(limit_page)
news_1 = naver_news_clipping_keyword(search_word, limit_page)

for i in range(len(news_1['title'])):
    print("제목:", news_1['title'][i])
    print("링크:", news_1['link'][i])
    print("내용:", news_1['contents'][i])
    print("언론사:", news_1['agency'][i])
    print("날짜&시간:", news_1['date'][i], news_1['time'][i])
    print("=======================")
