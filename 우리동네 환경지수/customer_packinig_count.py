import sqlite3
import pandas as pd

connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

# customer_code 리스트 추출
query = cursor.execute("SELECT DISTINCT(code) FROM tb_customer;")
cols = [column[0] for column in query.description]
customer_df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
customer_list = customer_df['code'].tolist() # 18675개

# 주문 정보에서 완료 주문인 행에 대하여 손님 코드, 포장 여부 추출
query = cursor.execute("SELECT customer_code, packaing FROM tb_order WHERE progress_status = '완료';")
cols = [column[0] for column in query.description]
order_df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# 손님코드별 포장비율 추출
output_df = pd.DataFrame(columns=['customer', 'packing_ratio', 'packing_cnt', 'all_cnt'])

for customer in customer_list:
    is_customer = order_df['customer_code'] == customer
    is_packing = order_df['packaing']=='Y' 

    all_df = order_df[is_customer] #특정 손님코드만 추출
    packing_df = order_df[is_customer & is_packing] #특정 손님코드 & 포장주문 추출

    if(len(all_df)!=0):
        packing_ratio = len(packing_df)/len(all_df)
        temp_df = pd.DataFrame([[customer, packing_ratio, len(packing_df), len(all_df)]], columns=['store', 'packing_ratio', 'packing_cnt', 'all_cnt'])
        output_df = pd.concat([output_df, temp_df], axis = 0)

output_df = output_df.sort_values('packing_cnt', ascending = False) #횟수 내림차순 정렬
output_df.to_csv("customer_packing.csv", index = False)