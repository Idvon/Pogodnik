import datetime

from requests import get

from src.compas import direction


def weather_data(city: dict) -> dict:
    call = get(
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={city['lat']}&longitude={city['lon']}&"
        "current_weather=true&"
        "windspeed_unit=ms&"
        "hourly=relativehumidity_2m"
    )
    data = call.json()
    current_time = data["current_weather"]["time"]
    list_time = data["hourly"]["time"]
    index_humidity = list_time.index(current_time)
    d = {
        "datetime": datetime.datetime.now(datetime.timezone.utc),
        "provider": "openmeteo",
        "city": city["name"],
        "state": city["state"],
        "country": city["country"],
        "temp": data["current_weather"]["temperature"],
        "hum": data["hourly"]["relativehumidity_2m"][index_humidity],
        "winddir": direction(int(data["current_weather"]["winddirection"])),
        "winddeg": int(data["current_weather"]["winddirection"]),
        "windspeed": data["current_weather"]["windspeed"],
    }
    return d
