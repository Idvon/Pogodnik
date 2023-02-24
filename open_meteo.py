import requests


def weather_data(city: dict) -> dict:
    lat = city['lat']
    lon = city['lon']
    call = requests.get("https://api.open-meteo.com/v1/forecast?"
                        f"latitude={lat}&longitude={lon}&"
                        "current_weather=true&"
                        "windspeed_unit=ms&"
                        "hourly=relativehumidity_2m")
    data = call.json()
    current_time = data['current_weather']['time']
    list_time = data['hourly']['time']
    index_humidity = list_time.index(current_time)
    d = {'city': city['name'],
         'country': city['country'],
         'state': city['state'],
         'temp': data['current_weather']['temperature'],
         'humidity': data['hourly']['relativehumidity_2m'][index_humidity],
         'windspd': data['current_weather']['windspeed'],
         'winddeg': int(data['current_weather']['winddirection']),
         'provider': 'Open-Meteo'}
    return d
