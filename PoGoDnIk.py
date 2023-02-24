import requests
import json
import open_weather
import conclusion
import open_meteo

with open("config.json") as f:
    config_data = json.load(f)
call_city = requests.get("https://api.openweathermap.org/geo/1.0/direct?"
                         f"q={config_data['city_name']}&"
                         "appid=2427c9b0a80567c0e8c21bdc1bd0b125")
city = json.loads(call_city.text)
city = city[0]
if len(city) == 0:
    print("This city is not found. Please, check city name.")
else:
    if config_data['provider_name'] == "openweather":
        data = open_weather.weather_data(city)
        print(conclusion.printing(data))
    if config_data['provider_name'] == "openmeteo":
        data = open_meteo.weather_data(city)
        print(conclusion.printing(data))
