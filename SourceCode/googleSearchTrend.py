from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import os

def google_search_trend():
    keyword = input("키워드를 입력하세요 : ")
    # 검색 기간 설정
    input_period = input("검색기간을 숫자로 입력해주세요(단위-Month) : ")
    period = "today {}-m".format(input_period)

    # matplotlib 한글폰트 오류 해결
    from matplotlib import font_manager, rc
    cwd = os.getcwd()
    font_path = os.path.join(cwd, "data", "malgun.ttf")
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    # Google Trend 접속
    trend_obj = TrendReq()
    trend_obj.build_payload(kw_list=[keyword], timeframe=period)

    # 시간에 따른 Trend 변화
    trend_df = trend_obj.interest_over_time()
    # print(trend_df.head())

    # 그래프로 시각화
    plt.style.use("ggplot")
    plt.figure(figsize=(14, 5))
    trend_df[keyword].plot()
    plt.title("Google Trends over time", size=15)
    plt.legend(labels=[keyword], loc="upper right")

    # 그래프 저장
    cwd = os.getcwd()
    output_filepath = os.path.join(cwd, "output", "google_trend_%s.png" % keyword)
    plt.savefig(output_filepath, dpi=300)
    plt.show()

if __name__ == "__main__":
    google_search_trend()