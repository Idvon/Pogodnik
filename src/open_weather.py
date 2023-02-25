import requests
from typing import Optional, Union


def weather_data(city, appid: Union[dict, str]) -> Optional[dict]:
    call = requests.get("https://api.openweathermap.org/data/2.5/weather?"
                        f"lat={city['lat']}&lon={city['lon']}&"
                        f"appid={appid}&"
                        "units=metric&")
    data = call.json()
    if data['cod'] != 200:
        return None
    else:
        d = {'city': city['name'],
             'country': city['country'],
             'state': city['state'],
             'temp': data['main']['temp'],
             'humidity': data['main']['humidity'],
             'windspd': data['wind']['speed'],
             'winddeg': data['wind']['deg'],
             'provider': 'Open Weather'}
        return d
