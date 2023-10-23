from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchCookieException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")


service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경



year = 2023
month = 9
set_title = set()
for i in range(24):
    ranking_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year,month)
    driver.get(ranking_url)
    datas = []
    time.sleep(0.5)
    for j in range(1,31):
        try:
            title_tag = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(j))
            title = title_tag.text
            if title in set_title:
                continue
            else:
                set_title.add(title)
            title_tag.click()
            time.sleep(1)
            review_tag = driver.find_element('xpath','//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
            review_tag.click()
            time.sleep(3)
            for k in range(5):
                more_button = driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')
                more_button.click()
                time.sleep(1)
            for k in range(1,160):
                try:
                    review = driver.find_element('xpath','/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k)).text
                    review = re.compile('[^가-힣]').sub(' ',review)
                    datas.append([title,review])
                except:
                    print('error {} {} {}'.format(i, j, k))
            ranking_url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(year, month)
            driver.get(ranking_url)
        except:
            print('error {} {}'.format(i,j))
    df_data = pd.DataFrame(datas,columns=['title','review'])
    df_data.to_csv('./crawling_data/review_{}{:02d}'.format(year,month),index=False)
    month-=1
    if month<=0:
        year-=1
        month=12

driver.close()


