import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/merge_reviews_professor.csv')
df.info()

# 형태소 분리
okt = Okt()

# 불용어 제거
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

count = 0
cleaned_sentences = []

for review in df.review:
    # 마냥 기다리기 그러니까 확인하려고
    count += 1
    if count % 100 == 0:
        print('.', end='')
    if count % 1000 == 0:
        print()
    if count % 10000 == 0:
        print(count/10000, end='')

    review = re.sub('[^가-힣]',' ', review)
    # 형태소 분리, 명사, 동사, 형용사만 남길 예정
    tokened_review = okt.pos(review, stem=True)     # pos: 튜플의 형태로 묶어줌.
    # print(tokened_review)       # [('사극', 'Noun'), ('으로서', 'Josa'), ('갖추다', 'Verb'), ('것', 'Noun'),....
    # exit()      #하나만 해보고 멈춰서 결과물 봐보자
    df_token = pd.DataFrame(tokened_review,columns=['word','class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class']=='Verb') |
                        (df_token['class']=='Adgective') ] # 조건 인덱싱
    # print(df_token.head())
    # exit()
    words = []
    for word in df_token.word:
        if 1<len(word): # 2글자 이상이고
            if word not in stopwords:   # 스탑워드스에 없는 경우
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
df = df[['title', 'cleaned_sentences']]
print(df.head(10))
df.info()

df.to_csv('./crawling_data/cleaned_review.csv', index=False)