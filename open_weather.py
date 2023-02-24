import requests
from typing import Union


def weather_data(city: dict[str, int]) -> dict[str, int]:
    lat = city['lat']
    lon = city['lon']
    call = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                        f"lat={lat}&lon={lon}&"
                        "appid=2427c9b0a80567c0e8c21bdc1bd0b125&"
                        "units=metric&")
    data = call.json()
    d = {'city': city['name'],
         'country': city['country'],
         'state': city['state'],
         'temp': data['main']['temp'],
         'humidity': data['main']['humidity'],
         'windspd': data['wind']['speed'],
         'winddeg': data['wind']['deg'],
         'provider': 'Open Weather'}
    return d
