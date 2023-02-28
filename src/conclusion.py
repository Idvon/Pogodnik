import csv
import os.path
from src.compas import direction


def printing(data, out_name: [dict, str]) -> str:
    if data is None:
        return "Please, check api key"
    else:
        if os.path.exists(out_name) is True:
            f = open(out_name, "a", newline='')
        else:
            f = open(out_name, "w", newline='')
        writer = csv.writer(f)
        writer.writerow([key for key in data])
        writer.writerow([data[key] for key in data])
        f.close()
        return f"Weather in {data['city']}\n" \
               f"Country: {data['country']}\n" \
               f"State: {data['state']}\n" \
               f"Temperature: {data['temp']} \N{degree sign}C\n" \
               f"Humidity: {data['hum']} %\n" \
               f"Wind speed: {data['windspeed']} m/s\n" \
               f"Wind direction: {direction(data['winddeg'])}\n" \
               f"By {data['provider']}"
