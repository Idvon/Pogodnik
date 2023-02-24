import requests
import statistics


def weather_data(city):
    lat = city['lat']
    lon = city['lon']
    call = requests.get("https://api.open-meteo.com/v1/forecast?"
                        f"latitude={lat}&longitude={lon}&"
                        "current_weather=true&"
                        "windspeed_unit=ms&"
                        "hourly=relativehumidity_2m")
    data = call.json()
    d = {'city': city['name'],
         'country': city['country'],
         'state': city['state'],
         'temp': data['current_weather']['temperature'],
         'humidity': int(statistics.mean(data['hourly']['relativehumidity_2m'])),
         'windspd': data['current_weather']['windspeed'],
         'winddeg': int(data['current_weather']['winddirection']),
         'provider': 'Open-Meteo'}
    return d
