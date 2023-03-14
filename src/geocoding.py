import requests
import json
from typing import Optional


def geo(geo_data: dict) -> Optional[dict]:
    call_city = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct?"
        f"q={geo_data['city_name']}&"
        f"appid={geo_data['api_key']}"
    )
    city = json.loads(call_city.text)
    if len(city) != 0:
        return city[0]
