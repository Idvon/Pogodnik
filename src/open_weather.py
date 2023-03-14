from requests import get
from src.compas import direction
from typing import Optional, Union
import datetime


def weather_data(city: dict, appid: str) -> Optional[dict]:
    call = get(
        "https://api.openweathermap.org/data/2.5/weather?"
        f"lat={city['lat']}&lon={city['lon']}&"
        f"appid={appid}&"
        "units=metric&"
    )
    data = call.json()
    if data["cod"] != 200:
        return None
    else:
        d = {
            "datetime": datetime.datetime.now(datetime.timezone.utc),
            "provider": "openweather",
            "city": city["name"],
            "state": city["state"],
            "country": city["country"],
            "temp": data["main"]["temp"],
            "hum": data["main"]["humidity"],
            "winddir": direction(data["wind"]["deg"]),
            "winddeg": data["wind"]["deg"],
            "windspeed": data["wind"]["speed"],
        }
        return d
