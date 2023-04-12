import abc
import csv
import datetime
from collections import namedtuple
from pathlib import Path
from typing import NamedTuple, Optional

from requests import get

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.output.compas import direction


class WeatherProvider(abc.ABC):
    url: str
    payload: dict

    def request(self) -> Optional[dict]:
        return get(self.url, params=self.payload).json()

    @abc.abstractmethod
    def weather_data(self, response) -> NamedTuple:
        """
        Parse response and return data structure
        """
        return namedtuple("weather_data", {})


class OpenWeatherWeatherProvider(WeatherProvider):
    def __init__(self, weather_config, coords: NamedTuple):
        self.payload = {
            "lat": coords.lat,
            "lon": coords.lon,
            "appid": weather_config["api_key"],
            "units": "metric",
        }
        self.url = "https://api.openweathermap.org/data/2.5/weather"

    def weather_data(self, response):
        if response["cod"] != 200:
            raise ProviderNoDataError("Please, check weather API key")
        lst = ["provider", "temp", "hum", "winddir", "winddeg", "windspeed"]
        weather_data = namedtuple("weather_data", lst)
        return weather_data(
            "openweather",
            response["main"]["temp"],
            response["main"]["humidity"],
            direction(response["wind"]["deg"]),
            response["wind"]["deg"],
            response["wind"]["speed"],
        )


class OpenMeteoWeatherProvider(WeatherProvider):
    def __init__(self, weather_config, coords: NamedTuple):
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
        lst = ["provider", "temp", "hum", "winddir", "winddeg", "windspeed"]
        weather_data = namedtuple("weather_data", lst)
        return weather_data(
            "openmeteo",
            response["current_weather"]["temperature"],
            response["hourly"]["relativehumidity_2m"][index_humidity],
            direction(int(response["current_weather"]["winddirection"])),
            int(response["current_weather"]["winddirection"]),
            response["current_weather"]["windspeed"],
        )


class CSVWeatherProvider(WeatherProvider):
    def __init__(self, file, timeout):
        self.current_time = datetime.datetime.now(datetime.timezone.utc)
        self.file = file
        self.timeout = timeout

    def weather_data(self, _=None) -> NamedTuple:
        with open(self.file, "r", newline="") as f:
            text = [row for row in csv.DictReader(f)]
            row = text[-1]
            last_time = datetime.datetime.fromisoformat(row["datetime"])
        delta = datetime.timedelta(seconds=self.timeout * 60)
        if (self.current_time - last_time) <= delta:
            weather_data = namedtuple("weather_data", row.keys())
            return weather_data._make(row.values())
        raise ProviderNoDataError("No data found in cache")


NET_PROVIDERS = {
    "openweather": OpenWeatherWeatherProvider,
    "openmeteo": OpenMeteoWeatherProvider,
}
LOCAL_PROVIDERS = {".csv": CSVWeatherProvider}


def create_net_weather_provider(
    weather_config: dict, coords: NamedTuple
) -> WeatherProvider:
    provider = weather_config["provider"]
    if provider in NET_PROVIDERS.keys():
        return NET_PROVIDERS[provider](weather_config, coords)
    raise ProviderCreationError("Please, check weather provider name")


# TODO: unify with previous function
def create_local_weather_provider(file: Path, timeout: int) -> CSVWeatherProvider:
    provider = file.suffix
    if provider in LOCAL_PROVIDERS.keys():
        return LOCAL_PROVIDERS[provider](file, timeout)
    raise ProviderCreationError("No local provider available")
