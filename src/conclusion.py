from src.compas import direction
from typing import Optional


def printing(data: Optional[dict]) -> str:
    if data is None:
        return "Please, check api key"
    else:
        return f"Weather in {data['city']}\n"\
               f"Country: {data['country']}\n"\
               f"State: {data['state']}\n"\
               f"Temperature: {data['temp']} \N{degree sign}C\n"\
               f"Humidity: {data['humidity']} %\n"\
               f"Wind speed: {data['windspd']} m/s\n"\
               f"Wind direction: {direction(data['winddeg'])}\n"\
               f"By {data['provider']}"
