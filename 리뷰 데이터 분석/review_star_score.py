import sqlite3
import pandas as pd

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
score_list = df['score']

score_list = list(map(int, score_list))
mean = sum(score_list) / len(score_list)
print(mean)