import requests
import json

CITY = "Daegu"
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

response = requests.get(url)
data = json.loads(response.text)
weather_condition = data["weather"][0]["description"]
temp = data["main"]["temp"]-273.15 #캘빈 온도 에서 섭씨 온도로 변환

if "rain" in weather_condition:
    print("비온다아이가 쿠폰 제공")

if temp>=35:
    print("덥다아이가 쿠폰 제공")