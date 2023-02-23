import requests
import json

with open("config.json", "r") as f:
    city = json.load(f)
call_city = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?"
                         f"q={city['city_name']}&"
                         f"appid=2427c9b0a80567c0e8c21bdc1bd0b125")
city_data = json.loads(call_city.text)
city_data = city_data[0]
lat = city_data['lat']
lon = city_data['lon']
call = requests.get(f"https://api.openweathermap.org/data/2.5/weather?"
                    f"lat={lat}&lon={lon}&"
                    f"appid=2427c9b0a80567c0e8c21bdc1bd0b125&"
                    f"units=metric&")
data = call.json()
print(f"Weather in {city['city_name']}\n"
      f"Temperature: {data['main']['temp']} C\N{degree sign}\n"
      f"Humidity: {data['main']['humidity']} %\n"
      f"Wind speed: {data['wind']['speed']} m/s\n"
      f"Wind direction: {data['wind']['deg']}\N{degree sign}")
