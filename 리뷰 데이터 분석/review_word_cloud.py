import sqlite3
import pandas as pd

from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import numpy as np
from PIL import *

connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

stop_list = ['맛있네요! 재주문의사★★★★★입니다~',
'배달 빠르고 맛도 좋습니다~ 잘 먹었습니다',
'음식이 정말 맛있네요~ 잘 먹었습니다!',
'맛있어요! 덕분에 든든한 식사 했습니다~',
'최고예요! 맛있는 음식 감사합니다.',
'맛있고 배달도 빠르네요~ 자주 주문할께요!',
'사장님 서비스 감사합니다.',
'배부르게 잘 먹었습니다~',
'맛있고 배달도 빠르네요~ 자주 주문할게요!',
'맛있게 잘 먹었습니다']

#포장 관련 리뷰 리스트 추출
query = cursor.execute("SELECT store_name, contents, date, score FROM tb_review WHERE (contents LIKE '%포장%')")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
temp_review_list = df['contents'].tolist()

#기본 멘트 제외
review_list = []
for review in temp_review_list:
    check = 1
    for stop_review in stop_list:
        if review in stop_review:
            check = 0
    if check==1:
        review_list.append(review)

# 빈출 단어(띄어쓰기)
cnt = 0
noun_list = []
for review in review_list:
    temp_list = review.split(' ')
    temp_list2 = []
    for i in temp_list:
        if(len(i)>1):
            temp_list2.append(i)

    noun_list += temp_list2

############### 빈출 단어(띄어쓰기, 형태소분석기) ####################
word_list = pd.Series(noun_list)
result = word_list.value_counts().head(200)

cand_mask=np.array(Image.open('circle.jpg'))
wordcloud = WordCloud(
    font_path = 'NanumGothicBold.ttf', # 한글 글씨체 설정
    background_color='white', # 배경색은 흰색으로 
    colormap='Greens', # 글씨색은 빨간색으로
    mask=cand_mask, # 워드클라우드 모양 설정
).generate_from_frequencies(result)
plt.figure(figsize=(5,5))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off') # 차트로 나오지 않게
plt.savefig('noun.png')