import csv
import os.path
from src.compas import direction


def printing(data, out_name: [dict, str]) -> str:
    if data is None:
        return "Please, check api key"
    else:
        text = None if os.path.exists(out_name) else data.keys()
        with open(out_name, "a", newline='') as f:
            writer = csv.writer(f)
            if text is not None:
                writer.writerow(text)
            writer.writerow(data.values())
        return f"Weather in {data['city']}\n" \
               f"Country: {data['country']}\n" \
               f"State: {data['state']}\n" \
               f"Temperature: {data['temp']} \N{degree sign}C\n" \
               f"Humidity: {data['hum']} %\n" \
               f"Wind speed: {data['windspeed']} m/s\n" \
               f"Wind direction: {direction(data['winddeg'])}\n" \
               f"By {data['provider']}"
