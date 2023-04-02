import csv
import datetime
import sqlite3
from pathlib import Path


def printing(city_data: dict) -> None:
    print(
        f"Weather in {city_data['city']}\n"
        f"Country: {city_data['country']}\n"
        f"State: {city_data['state']}\n"
        f"Temperature: {city_data['temp']} \N{degree sign}C\n"
        f"Humidity: {city_data['hum']} %\n"
        f"Wind speed: {city_data['windspeed']} m/s\n"
        f"Wind direction: {city_data['winddir']}\n"
        f"By {city_data['provider']}"
    )


def to_file(city_data: dict, out_file: Path) -> None:
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | city_data
    headers = None if out_file.is_file() else data.keys()
    with open(out_file, "a", newline="") as f:
        writer = csv.writer(f)
        if headers is not None:
            writer.writerow(headers)
        writer.writerow(data.values())


def sql_file(city_data: dict, db_file: Path) -> None:
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    data = date | city_data
    values = tuple(data.values())
    try:
        sqlite_connection = sqlite3.connect(db_file)
        headers = """
            CREATE TABLE if not exists weather_results (
            datetime date,
            provider text,
            temp real,
            hum integer,
            winddir text,
            winddeg integer,
            windspeed real,
            city text,
            state text,
            country text)
        """
        cursor = sqlite_connection.cursor()
        cursor.execute(headers)
        cursor.execute(
            "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values
        )
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(f"Error connecting to DB {error}")
    finally:
        sqlite_connection.close()
