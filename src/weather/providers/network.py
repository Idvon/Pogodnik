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
            "current": "relative_humidity_2m,"
                       "temperature_2m,"
                       "wind_speed_10m,"
                       "wind_direction_10m,",
            "wind_speed_unit": "ms",
        }
        self.url = "https://api.open-meteo.com/v1/forecast"

    def weather_data(self, response):
        return WeatherData(
            datetime.now(timezone.utc),
            "openmeteo",
            response["current"]["temperature_2m"],
            response["current"]["relative_humidity_2m"],
            direction(int(response["current"]["wind_direction_10m"])),
            int(response["current"]["wind_direction_10m"]),
            response["current"]["wind_speed_10m"],
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
