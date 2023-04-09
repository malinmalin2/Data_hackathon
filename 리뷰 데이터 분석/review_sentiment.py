import sqlite3
import pandas as pd
import csv
# from konlpy.tag import *

import numpy as np
from PIL import *
from NL_classifiers.review_classifier.restaurant_review_classifier import RestarantReviewClassifier

#https://github.com/good-jinu/NL-classifiers
connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

# 기본 멘트 리스트
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

query = cursor.execute("SELECT contents FROM tb_review" WHERE (contents LIKE '%포장%')")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
temp_review_list = df['contents'].tolist()
temp_review_list = [v for v in temp_review_list if v] #none 제거

#기본 멘트 제외
review_list = []
for review in temp_review_list:
    check = 1
    for stop_review in stop_list:
        if review in stop_review:
            check = 0
    if check==1:
        review_list.append(review)

clf = RestarantReviewClassifier()
output = clf.predict(review_list)
mean = sum(output) / len(output)
print(mean)