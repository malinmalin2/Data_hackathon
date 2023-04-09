import sqlite3
import pandas as pd

connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

# 날짜별 주문횟수
query = cursor.execute("SELECT count(*), strftime('%Y-%m-%d', order_date) FROM tb_order GROUP BY strftime('%Y-%m-%d', order_date);")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
df = df.sort_values("count(*)", ascending = False) #내림차순 정렬
df.to_csv("date_order.csv", index = False)

# 날짜별 포장횟수
query = cursor.execute("SELECT count(*), strftime('%Y-%m-%d', order_date) FROM tb_order where packaing=='Y' GROUP BY strftime('%Y-%m-%d', order_date);")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
df = df.sort_values("count(*)", ascending = False) #내림차순 정렬
df.to_csv("date_packing.csv", index = False)

# 요일+시간별 포장횟수
query = cursor.execute("SELECT count(*), strftime('%w', order_date), strftime('%H', order_date) FROM tb_order where packaing=='Y' GROUP BY strftime('%w', order_date), strftime('%H', order_date);")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
df = df.sort_values("count(*)", ascending = False) #내림차순 정렬
df.to_csv("day_time_packing.csv", index = False)

# 요일별 count
# query = cursor.execute("SELECT count(*), strftime('%w', order_date) FROM tb_order GROUP BY strftime('%w', order_date);")
# cols = [column[0] for column in query.description]
# df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# df = df.sort_values("count(*)", ascending = False) #내림차순 정렬
# df.to_csv("day_analysis.csv", index = False)

# 시간별 count
# query = cursor.execute("SELECT count(*), strftime('%H', order_date) FROM tb_order GROUP BY strftime('%H', order_date);")
# cols = [column[0] for column in query.description]
# df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# df = df.sort_values("count(*)", ascending = False) #내림차순 정렬
# df.to_csv("time_analysis.csv", index = False)