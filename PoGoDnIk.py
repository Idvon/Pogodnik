import requests
import json

with open("config.json", "r") as f:
    city = json.load(f)
call_city = requests.get("https://api.openweathermap.org/geo/1.0/direct?"
                         "q="+city["city_name"]+",ru&"
                         "appid=2427c9b0a80567c0e8c21bdc1bd0b125")
city_data = json.loads(call_city.text)
city_data = city_data[0]
lat = city_data["lat"]
lon = city_data["lon"]
call = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                    "lat="+str(lat)+"&lon="+str(lon)+"&"
                    "appid=2427c9b0a80567c0e8c21bdc1bd0b125&"
                    "units=metric&"
                    "lang=ru")
print(call.json())
