import requests
import json

with open("config.json", "r") as f:
    city = json.load(f)
call_city = requests.get("https://api.openweathermap.org/geo/1.0/direct?"
                         f"q={city['city_name']}&"
                         "appid=2427c9b0a80567c0e8c21bdc1bd0b125")
city_data = json.loads(call_city.text)
if len(city_data) == 0:
    print("This city not found. Please, check city name.")
else:
    city_data = city_data[0]
    lat = city_data['lat']
    lon = city_data['lon']
    call = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                        f"lat={lat}&lon={lon}&"
                        "appid=2427c9b0a80567c0e8c21bdc1bd0b125&"
                        "units=metric&")
    data = call.json()
    print(f"Weather in {city['city_name']}, Country: {city_data['country']}\n"
          f"Temperature: {data['main']['temp']} C\N{degree sign}\n"
          f"Humidity: {data['main']['humidity']} %\n"
          f"Wind speed: {data['wind']['speed']} m/s\n"
          f"Wind direction: {data['wind']['deg']}\N{degree sign}")
