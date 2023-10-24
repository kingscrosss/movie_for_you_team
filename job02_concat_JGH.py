import re
import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/review_*.csv')
# print(data_path)

df = pd.DataFrame()
for i in range(len(data_path)):
    df_temp = pd.read_csv(data_path[i])
    for j in range(len(df_temp['title'])):
        try:
            df_temp['title'][j] = re.compile('[^가-힣]').sub(' ', df_temp['title'][j])
            if (df_temp['title'][j].isspace()): df_temp['title'][j] = None
            df_temp['review'][j] = re.compile('[^가-힣]').sub(' ', df_temp['review'][j])
            if (df_temp['review'][j].isspace()): df_temp['review'][j] = None
        except:
            df_temp['review'][j] = None
            print(i, j)
    df = pd.concat([df, df_temp])
df.info()
df.to_csv('./crawling_data/crawling_review_1concat_{}.csv'.format(datetime.datetime.now().strftime('%y%m%d%H%M')), index = False)

# df = pd.read_csv('crawling_data/temp/crawling_review_1concat_2310231623.csv')
# df = df.dropna()
# print(df.info())
# df.to_csv('./crawling_data/crawling_review_2dropna{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index = False)
# df.drop_duplicates(['review'],inplace=True, keep='first')      # 리뷰 중복 제거
# print(df.info())
# df.to_csv('./crawling_data/crawling_review_3drop_duplicates{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index = False)