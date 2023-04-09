import requests
from urllib.parse import urlparse
import sqlite3
import pandas as pd
import pickle

connect = sqlite3.connect("OrderDB.db")
cursor = connect.cursor()

# 고유한 가맹점 리스트 추출, 11551개
query = cursor.execute("SELECT DISTINCT(store_name) FROM tb_order;")
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
store_list = df['store_name'].tolist()

# Kakao 지도 API를 활용하여 각 가맹점에 대한 음식 카테고리, id, 위도, 경도, 지번 주소 저장
output_df = pd.DataFrame(columns=['daeguro_store_name', 'food_category', 'id', 'lat', 'lng', 'address_name'])
for store in store_list:
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' + store
    result = requests.get(urlparse(url).geturl(), headers = {'Authorization': {API_KEY}}).json()
    
    if(result['documents']):
        match_first = result['documents'][0]
        if("대구" in match_first['address_name']): # 검색 결과가 존재하며 주소가 '대구'인 것에 대하여 저장
            food_category = ""
            if '>' in match_first['category_name']:
                food_category = match_first['category_name'].split('>')[1] # 음식군 정보 추출
            id = match_first['id'] # 가맹점 id
            lat = float(match_first['y']) # 위도
            lng = float(match_first['x']) # 경도
            address_name = match_first['address_name'] # 지번 주소
            temp_df = pd.DataFrame([[store, food_category, id, lat, lng, address_name]], columns=['daeguro_store_name', 'food_category', 'id', 'lat', 'lng' ,'address_name'])
            output_df = pd.concat([output_df, temp_df], axis = 0)

output_df.to_pickle("store_info.pickle")
output_df.to_csv("store_address_info.csv", index = False)