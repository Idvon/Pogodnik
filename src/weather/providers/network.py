from datetime import datetime, timezone

from src.exceptions import ProviderCreationError, ProviderNoDataError
from src.output.compas import direction
from src.structures import Coords, WeatherConfig, WeatherData
from src.weather.providers.base import WeatherProvider


class OpenWeatherWeatherProvider(WeatherProvider):
    def __init__(self, weather_config: WeatherConfig, coords: Coords):
        self.payload = {
            "lat": coords.lat,
            "lon": coords.lon,
            "appid": weather_config.api_key,
            "units": "metric",
        }
        self.url = "https://api.openweathermap.org/data/2.5/weather"

    def weather_data(self):
        if self.response["cod"] != 200:
            raise ProviderNoDataError("Please, check weather API key")
        return WeatherData(
            datetime.now(timezone.utc),
            "openweather",
            self.response["main"]["temp"],
            self.response["main"]["humidity"],
            direction(self.response["wind"]["deg"]),
            self.response["wind"]["deg"],
            self.response["wind"]["speed"],
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

    def weather_data(self):
        current_time = self.response["current_weather"]["time"]
        list_time = self.response["hourly"]["time"]
        index_humidity = list_time.index(current_time)
        return WeatherData(
            datetime.now(timezone.utc),
            "openmeteo",
            self.response["current_weather"]["temperature"],
            self.response["hourly"]["relativehumidity_2m"][index_humidity],
            direction(int(self.response["current_weather"]["winddirection"])),
            int(self.response["current_weather"]["winddirection"]),
            self.response["current_weather"]["windspeed"],
        )


NET_PROVIDERS = {
    "openweather": OpenWeatherWeatherProvider,
    "openmeteo": OpenMeteoWeatherProvider,
}


def create_net_weather_provider(
    weather_config: WeatherConfig, coords: Coords
) -> WeatherProvider:
    provider = weather_config.provider
    if provider in NET_PROVIDERS.keys():
        return NET_PROVIDERS[provider](weather_config, coords)
    raise ProviderCreationError("Please, check weather provider name")
