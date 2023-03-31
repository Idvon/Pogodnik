import csv
import datetime
import sqlite3
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


def to_file(city_data: dict, out_file: Path):
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | city_data
    headers = None if out_file.is_file() else data.keys()
    with open(out_file, "a", newline="") as f:
        writer = csv.writer(f)
        if headers is not None:
            writer.writerow(headers)
        writer.writerow(data.values())


def sql_file(city_data: dict):
    file = "db.sqlite3"
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | city_data
    data = tuple(data.values())
    print(data)
    print(type(data))
    try:
        sqlite_connection = sqlite3.connect(file)
        headers = "create table if not exists weather_results (" \
                  "date date," \
                  "provider text," \
                  "temp real," \
                  "hum integer," \
                  "winddir text," \
                  "winddeg integer," \
                  "windspeed real," \
                  "city text," \
                  "state text," \
                  "country text);"
        cursor = sqlite_connection.cursor()
        print("DB connect to SQLite")
        cursor.execute(headers)
        cursor.execute("insert into weather_results(date, provider, temp, hum, winddir, winddeg, windspeed, city, state, country)"
                       "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        sqlite_connection.commit()
        print("DB creation")
        cursor.close()
    except sqlite3.Error as error:
        print(f"Error connecting to DB {error}")
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Connecting with SQLite close")


if __name__ == "__main__":
    q = {"datetime": datetime.datetime.fromisoformat("2023-03-26 15:56:47.080217+00:00"),
         "provider": "openweather",
         "temp": 2.04,
         "hum": 93,
         "winddir": "NE",
         "winddeg": 50,
         "windspeed": 4,
         "city": "Saint Petersburg",
         "state": "Saint Petersburg",
         "country": "RU"}
    sql_file(q)
