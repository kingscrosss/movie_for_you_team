import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    moviIdx = [i[0] for i in simScore]
    recMovielist = df_reviews.iloc[moviIdx, 0]
    return recMovielist

df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle','rb') as f:
    Tfidf = pickle.load(f)

# # 영화 리뷰 기반 추천
# print(df_reviews.iloc[383,0])
# cosine_sim = linear_kernel(Tfidf_matrix[383], Tfidf_matrix)       # 코사인 유사도
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# # keyword 기반 추천
# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model') # 모델 불러오기
# keyword = '겨울'
# try:
#     sim_word = embedding_model.wv.most_similar(keyword,topn=10)
#     print(sim_word)
#     words = [keyword]
#     for word, _ in sim_word:
#         words.append(word)
#     print(words)
#
#     sentence = []
#     count = 10      # 마블 키워드의 갯수
#     for word in words:
#         sentence = sentence + [word]*count  # 가중치 반영을 위해서, 앞에 있을수록 유사도가 높으니까
#         count -= 1
#     sentence=' '.join(sentence)
#     print(sentence)
#
#     sentence_vec = Tfidf.transform([sentence])
#     cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
#     recommendation = getRecommendation(cosine_sim)
#     print(recommendation)
#
# except:
#     print("추천 영화가 존재하지 않습니다.")

# 문장으로 입력 받을 경우
## 문장 전처리
needs = '화려한 액션과 소름 돋는 반전이 있는 영화'
cleaned_needs = []
# 형태소 분리
okt = Okt()
# 불용어 제거
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

needs = re.sub('[^가-힣]',' ', needs)       # 리뷰만 해줌
# 형태소 분리, 명사, 동사, 형용사만 남길 예정
tokened_needs = okt.pos(needs, stem=True)     # pos: 튜플의 형태로 묶어줌.
# print(tokened_sentence)
df_token = pd.DataFrame(tokened_needs,columns=['word','class'])
df_token = df_token[(df_token['class']=='Noun') |
                    (df_token['class']=='Verb') |
                    (df_token['class']=='Adgective') ] # 조건 인덱싱
# print(df_token.head())
needs_words = []
for needs_word in df_token.word:
    if 1<len(needs_word): # 2글자 이상이고
        if needs_word not in stopwords:   # 스탑워드스에 없는 경우
            needs_words.append(needs_word)
    # cleaned_needs = ' '.join(needs_words)
print(needs_words)

## 추천
embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# keyword = needs_words[0]
try:
    wordss = []
    for keyword in needs_words:
        sim_word = embedding_model.wv.most_similar(keyword,topn=10)
        # print(sim_word)
        words = [keyword]
        # print(words)
        for word, _ in sim_word:
            words.append(word)
        wordss = wordss + words
    print(wordss)
    sentence = []
    count = len(wordss)
    for word in wordss:
        sentence = sentence + [word]*count  # 가중치 반영을 위해서, 앞에 있을수록 유사도가 높으니까
        count -= 1
    sentence=' '.join(sentence)
    print(sentence)

    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    recommendation = getRecommendation(cosine_sim)
    print(recommendation)
except:
    print("추천 영화가 존재하지 않습니다.")