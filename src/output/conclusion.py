import csv
import datetime
from pathlib import Path


def printing(geo_data: dict, weather_data: dict) -> str:
    data = weather_data | geo_data
    return (
        f"Weather in {data['city']}\n"
        f"Country: {data['country']}\n"
        f"State: {data['state']}\n"
        f"Temperature: {data['temp']} \N{degree sign}C\n"
        f"Humidity: {data['hum']} %\n"
        f"Wind speed: {data['windspeed']} m/s\n"
        f"Wind direction: {data['winddir']}\n"
        f"By {data['provider']}"
    )


def in_file(geo_data: dict, weather_data: dict, out_file: Path):
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | weather_data | geo_data
    headers = None if out_file.is_file() else data.keys()
    with open(out_file, "a", newline="") as f:
        writer = csv.writer(f)
        if headers is not None:
            writer.writerow(headers)
        writer.writerow(data.values())
