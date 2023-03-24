import csv
import datetime
from pathlib import Path


def printing(city_data: dict) -> str:
    return (
        f"Weather in {city_data['city']}\n"
        f"Country: {city_data['country']}\n"
        f"State: {city_data['state']}\n"
        f"Temperature: {city_data['temp']} \N{degree sign}C\n"
        f"Humidity: {city_data['hum']} %\n"
        f"Wind speed: {city_data['windspeed']} m/s\n"
        f"Wind direction: {city_data['winddir']}\n"
        f"By {city_data['provider']}"
    )


def in_file(city_data: dict, out_file: Path):
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | city_data
    headers = None if out_file.is_file() else data.keys()
    with open(out_file, "a", newline="") as f:
        writer = csv.writer(f)
        if headers is not None:
            writer.writerow(headers)
        writer.writerow(data.values())
