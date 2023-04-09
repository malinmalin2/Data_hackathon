import sqlite3
import pandas as pd
import csv

connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

# 행정동 리스트 추출
query = cursor.execute("SELECT DISTINCT(district2) FROM tb_customer;")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
district_list = df['district2'].tolist()

# 고객 코드를 key로 하여 주문정보(tb_order)와 고객정보(tb_customer) 테이블 조인
# 매핑되는 주문 정보에 대하여 고객 코드, 행정동 정보, 포장 여부 추출
query = cursor.execute("SELECT tb_order.customer_code, tb_order.packaing, tb_customer.district1, tb_customer.district2 FROM tb_order INNER JOIN tb_customer ON tb_order.customer_code = tb_customer.code;")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# 각 행정동별 포장비율 계산
output_df = pd.DataFrame(columns=['district1', 'district2', 'packing_ratio', 'packing_cnt', 'all_cnt'])
for district in district_list:
    df_district = df['district2'] == district
    all_df = df[df_district] # 특정 행정동에 대한 주문정보 추출
    
    df_packing = df['packaing']=='Y'
    packing_df = df[df_district & df_packing] # 특정 행정동 & 포장주문정보 추출

    if(len(all_df)!=0):
        packing_ratio = len(packing_df)/len(all_df) # 포장비율 계산
        district1_info = df.loc[df["district2"]==district, ["district1"]].values[0].item() # 구 정보 추출
        output_df = output_df.append(pd.DataFrame([[district1_info, district, packing_ratio, len(packing_df), len(all_df)]], columns=['district1', 'district2', 'packing_ratio', 'packing_cnt', 'all_cnt']))

output_df = output_df.sort_values('packing_ratio', ascending = False) #포장 비율에 대한 내림차순 정렬
output_df.to_csv("packing.csv", index = False)