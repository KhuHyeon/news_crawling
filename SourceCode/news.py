class News:
    numCreatedNews = 0
    def __init__(self, title, link, contents, agency, date, time):
        self.title = title
        self.link = link
        self.contents = contents
        self.agency = agency
        self.date = date
        self.time = time
        News.numCreatedNews += 1

    def print(self):
        print("제목:", self.title)
        print("링크:", self.link)
        print("내용:", self.contents)
        print("언론사:", self.agency)
        print("날짜&시간:", self.date, self.time)
        print("=====================================================")

    # 주어진 날짜 사이에 있으면 true 아니면 false
    def is_indate(self, start, end):
        if start <= self.date and self.date <= end:
            return True
        else:
            return False
