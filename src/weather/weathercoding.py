import abc
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.output.compas import direction
from src.structures import Coords, GeoData, WeatherConfig, WeatherData


class WeatherProvider(abc.ABC):
    url: str
    payload: dict

    def request(self) -> Optional[dict]:
        return get(self.url, params=self.payload).json()

    @abc.abstractmethod
    def weather_data(self, response: Optional[dict]) -> WeatherData:
        """
        Parse response and return data structure
        """
        return WeatherData._make({})


class OpenWeatherWeatherProvider(WeatherProvider):
    def __init__(self, weather_config: WeatherConfig, coords: Coords):
        self.payload = {
            "lat": coords.lat,
            "lon": coords.lon,
            "appid": weather_config.api_key,
            "units": "metric",
        }
        self.url = "https://api.openweathermap.org/data/2.5/weather"

    def weather_data(self, response):
        if response["cod"] != 200:
            raise ProviderNoDataError("Please, check weather API key")
        return WeatherData(
            datetime.now(timezone.utc),
            "openweather",
            response["main"]["temp"],
            response["main"]["humidity"],
            direction(response["wind"]["deg"]),
            response["wind"]["deg"],
            response["wind"]["speed"],
        )


class OpenMeteoWeatherProvider(WeatherProvider):
    def __init__(self, weather_config: WeatherConfig, coords: Coords):
        self.payload = {
            "latitude": coords.lat,
            "longitude": coords.lon,
            "current_weather": "true",
            "windspeed_unit": "ms",
            "hourly": "relativehumidity_2m",
        }
        self.url = "https://api.open-meteo.com/v1/forecast"

    def weather_data(self, response):
        current_time = response["current_weather"]["time"]
        list_time = response["hourly"]["time"]
        index_humidity = list_time.index(current_time)
        return WeatherData(
            datetime.now(timezone.utc),
            "openmeteo",
            response["current_weather"]["temperature"],
            response["hourly"]["relativehumidity_2m"][index_humidity],
            direction(int(response["current_weather"]["winddirection"])),
            int(response["current_weather"]["winddirection"]),
            response["current_weather"]["windspeed"],
        )


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


NET_PROVIDERS = {
    "openweather": OpenWeatherWeatherProvider,
    "openmeteo": OpenMeteoWeatherProvider,
}
LOCAL_PROVIDERS = {".sqlite3": DBWeatherProvider}


def create_net_weather_provider(
    weather_config: WeatherConfig, coords: Coords
) -> WeatherProvider:
    provider = weather_config.provider
    if provider in NET_PROVIDERS.keys():
        return NET_PROVIDERS[provider](weather_config, coords)
    raise ProviderCreationError("Please, check weather provider name")


# TODO: unify with previous function
def create_local_weather_provider(
    file: Path, city: str, timeout: int
) -> DBWeatherProvider:
    provider = file.suffix
    if provider in LOCAL_PROVIDERS.keys():
        return LOCAL_PROVIDERS[provider](file, city, timeout)
    raise ProviderCreationError("No local provider available")
