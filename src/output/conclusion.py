import abc
import csv
import sqlite3
from pathlib import Path

from src.exceptions import ProviderCreationError
from src.structures import GeoData, WeatherData


class CityData(abc.ABC):
    def __init__(self, weather_data: WeatherData, geo_data: GeoData, file_out: Path):
        self.weather_data = weather_data
        self.geo_data = geo_data
        self.file_out = file_out

    @abc.abstractmethod
    def city_outputs(self) -> dict:
        """
        Data retrieval and output in different file formats
        """
        return {}


class CSVFileWriter(CityData):
    def city_outputs(self):
        headers = self.weather_data._fields + self.geo_data._fields
        headers = None if self.file_out.is_file() else headers
        with open(self.file_out, "a", newline="") as f:
            writer = csv.writer(f)
            if headers is not None:
                writer.writerow(headers)
            values = *self.weather_data, *self.geo_data
            writer.writerow(values)


class DatabaseWriter(CityData):
    def city_outputs(self):
        values = *self.weather_data, *self.geo_data
        try:
            sqlite_connection = sqlite3.connect(self.file_out)
            headers = """
                CREATE TABLE IF NOT EXISTS weather_results (
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


WRITER = {".csv": CSVFileWriter, ".sqlite3": DatabaseWriter}


def create_output_format(
    weather_data: WeatherData, geo_data: GeoData, file_out: Path
) -> CityData:
    form = file_out.suffix
    if form in WRITER.keys():
        return WRITER[form](weather_data, geo_data, file_out)
    raise ProviderCreationError("No local provider available")


def to_display(weather_data: WeatherData, geo_data: GeoData) -> None:
    print(
        f"Weather in {geo_data.city}\n"
        f"Country: {geo_data.country}\n"
        f"State: {geo_data.state}\n"
        f"Temperature: {weather_data.temp} \N{degree sign}C\n"
        f"Humidity: {weather_data.hum} %\n"
        f"Wind speed: {weather_data.windspeed} m/s\n"
        f"Wind direction: {weather_data.winddir}\n"
        f"By {weather_data.provider}"
    )
