import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.structures import GeoData, WeatherData
from src.weather.providers.base import WeatherProvider


class DBWeatherProvider(WeatherProvider):
    def __init__(self, file: Path, city: str, timeout: int):
        self.file = file
        self.timeout = timeout
        self.city = city

    def weather_data(self, _=None):
        delta = timedelta(seconds=self.timeout * 60)
        try:
            sqlite_connection = sqlite3.connect(self.file)
            cursor = sqlite_connection.cursor()
            cursor.execute(
                """
                SELECT
                datetime,
                provider,
                temp,
                hum,
                winddir,
                winddeg,
                windspeed,
                city,
                country,
                state
                FROM weather_results WHERE city = ?
                """,
                (self.city,),
            )
            row = cursor.fetchall()
            if len(row) == 0:
                raise ProviderNoDataError("No data found in cache")
            data = row[-1]
            weather_data = WeatherData(
                datetime.fromisoformat(data[0]),
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
            )
            geo_data = GeoData(data[7], data[8], data[9])
            cursor.close()
        except sqlite3.Error as error:
            print(f"Error connecting to DB {error}")
        finally:
            sqlite_connection.close()
        current_time = datetime.now(timezone.utc)
        last_time = weather_data.datetime
        if (current_time - last_time) <= delta:
            return weather_data, geo_data
        raise ProviderNoDataError("No data found in cache")


LOCAL_PROVIDERS = {".sqlite3": DBWeatherProvider}


def create_local_weather_provider(
    file: Path, city: str, timeout: int
) -> DBWeatherProvider:
    provider = file.suffix
    if provider in LOCAL_PROVIDERS.keys():
        return LOCAL_PROVIDERS[provider](file, city, timeout)
    raise ProviderCreationError("No local provider available")
