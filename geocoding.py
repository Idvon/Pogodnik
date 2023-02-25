import requests
import json
from typing import Optional


def geo(config_data: dict) -> Optional[dict]:
    call_city = requests.get("https://api.openweathermap.org/geo/1.0/direct?"
                             f"q={config_data['city_name']}&"
                             f"appid={config_data['geo_provider']['api_key']}")
    city = json.loads(call_city.text)
    if len(city) != 0:
        return city[0]
