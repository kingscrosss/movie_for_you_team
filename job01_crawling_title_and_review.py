# 다음 영화 - 랭킹 - 박스오피스 - 월간 크롤링
# 1) 영화 별로 들어가서 평점 더보기 5번 누른 후 스크립할 것
# 2) 다음 달로 넘어가서 반복진행
# 월간 -> 영화 클릭 -> 평점 클릭 -> 더보기 버튼 x5번 -> 뒤로가기 두번 -> 월 이동 후 반복
# 월간 페이지 주소: 마지막이 년도+월
# https://movie.daum.net/ranking/boxoffice/monthly?date=202309
# https://movie.daum.net/ranking/boxoffice/monthly?date=202308
# 영화 제목(li[?]부분)
# /html/body/div[2]/main/article/div/div[2]/ol/li[1]/div/div[2]/strong/a
# /html/body/div[2]/main/article/div/div[2]/ol/li[2]/div/div[2]/strong/a
# 페이지 들어간 후 제목(변화X)
# /html/body/div[2]/main/article/div/div[1]/div[2]/div[1]/h3/span[1]
# /html/body/div[2]/main/article/div/div[1]/div[2]/div[1]/h3/span[1]
# 평점 버튼(변화x)
# /html/body/div[2]/main/article/div/div[2]/div[1]/ul/li[4]/a/span
# /html/body/div[2]/main/article/div/div[2]/div[1]/ul/li[4]/a/span
# 평점 더보기 버튼(변화x)
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[1]/button
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[1]/button
# 후기 내용(li[?]부분)
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[73]/div/p
# /html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[60]/div/p

# 파일 맨 뒤에 년도 붙이기
# 최종 형태: title - review 로 컬럼명

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import glob
import re
import time

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

year = 2021
for year in range(2021, 2023):
    for month in range(6, 13):
            titles = []
            reviews = []
            for j in range(1, 31):  # 랭킹 1~30까지
                try:
                    # 월간 페이지
                    url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year,month)   # https://movie.daum.net/ranking/boxoffice/monthly?date=202309
                    driver.get(url)
                    time.sleep(0.5)
                    driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(j)).click()
                except:
                    print("영화 접속 에러")
                    continue
                # 제목 크롤링
                title = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[1]/div[2]/div[1]/h3/span[1]')
                title = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', title.text)
                # 평점 클릭
                driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[1]/ul/li[4]/a').click()
                driver.refresh()
                # 더보기 5번
                for i in range(5):
                    try:
                        time.sleep(0.5)
                        driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
                    except: print(title, '더보기 error :', url)
                for i in range(1,161):
                    try:
                        review = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(i))
                        review = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review.text)
                        print(title, review)
                        titles.append(title)
                        reviews.append(review)
                        review = []
                    except: print(title,'review errer')
                title = []

            df_data = pd.DataFrame(titles, columns=['title'])
            df_data['review'] = reviews
            df_data.to_csv('./crawling_data/review_{}{:02d}.csv'.format(year,month),index=False)

driver.close()