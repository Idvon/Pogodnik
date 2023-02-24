import requests
import json
from typing import Union


def geo(config_data: dict[str, str]) -> Union[dict[str, int], int]:
    call_city = requests.get("https://api.openweathermap.org/geo/1.0/direct?"
                             f"q={config_data['city_name']}&"
                             "appid=2427c9b0a80567c0e8c21bdc1bd0b125")
    city = json.loads(call_city.text)
    if len(city) != 0:
        return city[0]
    else:
        return 0
