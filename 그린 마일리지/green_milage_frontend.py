import requests
import pickle
import json
import streamlit as st
import requests
from haversine import haversine
from PIL import Image


def main():
    st.title("그린 마일리지")
    with open("store_info.pickle", "rb" ) as file:
        df = pickle.load(file)
    
    # 출발지는 임의로 경북대학교 누리관으로 설정
    # 누리관의 정보는 다음과 같으며 카카오맵에서 사용하는 x, y 좌표 정보를 활용하였음
    # ID = 443117484
    home_x = 128.61356021837153
    home_y = 35.89348464660513

    sX = '864215'
    sY = '668572'

    # 구 선택
    gu = ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군']
    selected_gu = st.selectbox('구를 선택하세요.', gu)
    if(selected_gu):
        dong = []
        if(selected_gu == '중구'):
            dong = ['동인동', '삼덕동', '성내동', '대신동', '남산동', '대봉동']
        elif(selected_gu == '동구'):
            dong = ['신암동', '신천동', '효목동', '도평동', '불로봉무동', '지저동', '동촌동', '방촌동', '해안동', '안심동', '혁신동', '공산동']
        elif(selected_gu == '서구'):
            dong = ['내당동', '비산동', '평리동', '상중이동', '원대동']
        elif(selected_gu == '남구'):
            dong = ['이천동', '봉덕동', '대명동']
        elif(selected_gu == '북구'):
            dong = ['고성동', '칠성동', '침산동', '노원동', '산격동' ,'복현동', '대현동', '검단동', '무태조야동', '관문동', '태전동','구암동', '관음동', '읍내동' , '동천동' ,'국우동']
        elif(selected_gu == '수성구'):
            dong = ['범어동', '만촌동', '황금동', '중동', '상동', '파동', '두산동', '지산동', '범물동', '고산동']
        elif(selected_gu == '달서구'):
            dong = ['성당동', '두류동', '본리동', '감삼동', '죽전동', '장기동', '용산동', '이곡동', '신당동', '월성동', '진천동', '유천동', '상인동', '도원동', '송현동', '본동']
        elif(selected_gu == '달성군'):
            dong = ['화원읍', '논공읍', '다사읍', '유가읍', '옥포읍', '현풍읍', '가창면', '하빈면', '구지면']

        selected_dong = st.selectbox('동을 선택하세요.', dong)

        # selected_dong을 주소로 갖고 있는 가게 리스트 정보 제공
        is_selected_dong = df['address_name'].str.contains(selected_dong)
        selected_dong_df = df[is_selected_dong]
        store_list = selected_dong_df['daeguro_store_name'].values.tolist()

        selected_store = st.selectbox('가게를 선택하세요.', store_list)

        # 선택한 가게에 대한 가게 정보
        store_info = selected_dong_df[selected_dong_df['daeguro_store_name']==selected_store]
        
        # 가게 id, 위도, 경도
        id = store_info.iloc[0]['id']
        store_y = store_info.iloc[0]['lat'] #위도(y)
        store_x = store_info.iloc[0]['lng'] #경도(x)

        # 도착지에 대한 x, y 좌표 정보를 활용하기 위해 호출 후 파싱하여 얻음
        url = 'https://map.kakao.com/link/to/'+ id
        r = requests.post(url)
        url_parse = r.url.split("%2C")
        eX = url_parse[2]
        eY = url_parse[3].split('&')[0]

        # 카카오맵 api와 출발지와 도착지 x, y 좌표를 활용하여 도보 거리, 도보 시간, 소모 칼로리 정보, 가는길 정보 제공
        walk_url = 'https://map.kakao.com/route/walkset.json?callback=&sName=&sX=' + sX + '&sY=' + sY + '&eName=&eX=' +eX + '&eY=' + eY + '&ids=,'
        response = requests.get(walk_url)
        calories = json.loads(response.text)['directions'][1]['sections'][0]['calories']
        time = (json.loads(response.text)['directions'][1]['sections'][0]['time'])/60

        walk_distance = json.loads(response.text)['directions'][1]['sections'][0]['length']
        calories = json.loads(response.text)['directions'][1]['sections'][0]['calories']
        time = (json.loads(response.text)['directions'][1]['sections'][0]['time'])/60
        milage = walk_distance * 0.1

        st.subheader("포장할 경우 그린 마일리지 " + str(round(milage, 1)) + "원을 드려요!")
        st.subheader("도보 " + str(round(time, 2)) +"분 소요됩니다")
        st.subheader("포장할 경우 " + str(calories) +"kcal를 소모할 수 있어요!")

        if st.button('포장하러 가는 길 보기'):
            help_url = 'https://map.kakao.com/?map_type=TYPE_MAP&target=walk&rt=' + sX + ',' + sY + ',' + eX + ',' + eY
            html = f'<iframe width="100%" height="500" src={help_url} frameborder="0"></iframe>'
            st.write(html, unsafe_allow_html=True)

        if st.button('우리동네 양산지도'):
            img = Image.open(selected_gu+'.png')
            st.image(img)

        # 선택한 음식점 반경 2km 내에 있는 공원 최대 10개 호출
        url = 'https://apis.data.go.kr/6270000/dgInParkwalk/getDgWalkParkList?serviceKey=PaAFGMyZ6ss9GELl1ObizCXFxU3KilWKN07%2BYAbkkmsZYdAlD46jwcuMh9%2B23rWs1r5VciO49fbFlVAeFRFUlQ%3D%3D&pageNo=1&numOfRows=10&type=json&lat=' + str(store_y) + '&lot=' + str(store_x) + '&radius=2'
        response = requests.get(url)
        data_json = json.loads(response.text)
        body = data_json.get("body")
        park_nums = body["totalCount"]
        store_info = (float(store_y), float(store_x))
        now_distance = 5

        # 반환된 공원 중 거리가 가장 가까운 공원 선택
        for park_num in range(park_nums):
            temp_y = body["items"]["item"][park_num]["lat"]
            temp_x = body["items"]["item"][park_num]["lot"]
            temp_name = body["items"]["item"][park_num]['parkNm']
            park_info = (float(temp_y), float(temp_x))
            temp_distance = haversine(store_info, park_info, unit = 'km')
            if(temp_distance < now_distance):
                now_distance = temp_distance
                park_y = temp_y
                park_x = temp_x
                park_name = temp_name

        # api 호출로 반환된 공원이 1개 이상일 경우 공원 추천
        if(park_num>=1):
            url = 'https://map.kakao.com/link/map/'+str(park_y) +','+str(park_x)
            store_info = (float(store_y), float(store_x))
            park_info = (float(park_y), float(park_x))
            distance = haversine(store_info, park_info, unit = 'km')
            st.subheader(selected_store + "과 " + str(round(distance, 2)) + 'km 떨어진 곳에 ' + park_name + '이 있어요! 산책 어때요?')
            if st.button('공원 구경하기'):
                html = f'<iframe width="100%" height="500" src="https://map.kakao.com/link/map/{park_y},{park_x}" frameborder="0"></iframe>'            
                st.write(html, unsafe_allow_html=True)
main()