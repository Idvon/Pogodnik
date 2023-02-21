import requests
import json

call_city = requests.get('https://api.openweathermap.org/geo/1.0/direct?'
                 'q=Saint Petersburg,ru&'
                 'appid=2427c9b0a80567c0e8c21bdc1bd0b125', 'r')
city_data = json.loads(call_city.text)
city_data = dict(city_data[0])
#city_data = json.load(city_data[0])
lat = 1
lon = 1
#call = requests.get("https://api.openweathermap.org/data/2.5/weather?"
#                    "q=Saint Petersburg"
#                    "appid=2427c9b0a80567c0e8c21bdc1bd0b125&"
#                    "units=metric&"
#                    "lang=ru")
#print(call.json())
print(type(city_data))
print(city_data)

url = 'http://api.open-notify.org/iss-now.json'
response = requests.get(url)
text = response.text
dicti = json.loads(text)
print(text)
print(type(dicti))
print(dicti)

