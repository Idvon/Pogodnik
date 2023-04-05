import abc
import csv
import datetime
import sqlite3
from pathlib import Path

from src.exceptions import ProviderCreationError


class WeatherData(abc.ABC):
    def __init__(self, city_data: dict, file_out: Path):
        self.city_data = city_data
        self.file_out = file_out
        print(1)

    @abc.abstractmethod
    def weather_outputs(self, city_data, file_out) -> dict:
        """
        Data retrieval and output in different file formats
        """
        return {}


class ToCSVFile(WeatherData):
    def weather_outputs(self, city_data, file_out):
        headers = None if self.file_out.is_file() else self.city_data.keys()
        with open(self.file_out, "a", newline="") as f:
            writer = csv.writer(f)
            if headers is not None:
                writer.writerow(headers)
            writer.writerow(self.city_data.values())


class ToDataBase(WeatherData):
    def weather_outputs(self, city_data, file_out):
        values = tuple(self.city_data.values())
        try:
            sqlite_connection = sqlite3.connect(self.file_out)
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
                "INSERT INTO weather_results VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                values,
            )
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(f"Error connecting to DB {error}")
        finally:
            sqlite_connection.close()


FORMATS = {".csv": ToCSVFile, ".sqlite3": ToDataBase}


def create_output_format(city_data: dict, file_out: Path) -> WeatherData:
    date = {"datetime": datetime.datetime.now(datetime.timezone.utc)}
    city_data = date | city_data
    form = file_out.suffix
    if form in FORMATS.keys():
        return FORMATS[form](city_data, file_out)
    raise ProviderCreationError("No local provider available")


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
