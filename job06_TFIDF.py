# TF-IDF(Term Frequency - Inverse Document Frequency): 정보 검색과 텍스트 마이닝에서 이용하는 가중치
# 즉, 모든 문장(Document)에서 자주 나오는 단어는 가중치를 낮게 주고 한 문장에서 자주 나오는 단어는 가중치를 높게 주는 것을 TFIDF
# * text frequency, document frequency
#   1) 직업: 개발자, 나이: 40, 성별: 남자
#   2) 직업: 디자이너, 나이: 40, 성별: 여자
#   3) 직업: 개발자, 나이: 40, 성별: 여자
#   4) 직업: 디자이너, 나이: 30, 성별: 남자
# 1번과 가장 유사한 사람은? 3번.
# 사유: 값이 가장 유사하니까
# 그렇지만 값이 무조건 들어가있는 직업, 나이, 성별은 무시함 -> df
# 문장 안에 다 있는 값은 유사값에 반비례로 처리 ex) df
# 다른 문장엔 없고 1,3번에 공통으로 들어간 경우만 유사 점수를 비례하게 준다. -> tf
# tf*(1/df) 값을 곱해서 준다
# 두 단어간의 상관관계를 벡터로 나타내면 cos으로 표현하였을 때 1에 가까우면 유사, 0에 가까우면 관련 x, -1이면 반대로 이를 cos유사도라 함.


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread        # mmwrite: 메트릭스를 저장하는 패키지
import pickle

df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])       # reviews 안에 몇 개의 형태소를 가졌는지
print(Tfidf_matrix.shape)   # (1935, 44667) 리뷰가 1935개가 있고 그것에 유니크한 단어가 44667개를 가진다.

with open('./models/tfidf.pickle','wb') as f:
    pickle.dump(Tfidf,f)
mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)

# len(df['title'].unique()) = 1935