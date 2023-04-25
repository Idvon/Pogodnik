from datetime import datetime, timezone

from freezegun import freeze_time
from pytest import fixture

from src.config_file_parser.file_parser import WeatherConfig
from src.geo.geocoding import Coords
from src.weather.weathercoding import (
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    WeatherData,
    create_net_weather_provider,
)
from tests.conftest import MockResponse
from tests.unit.constants import OM_RESPONSE, OW_RESPONSE

GET_PATH = "src.weather.weathercoding.get"


@fixture
def mock_openmeteo_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OM_RESPONSE, 200))


@fixture
def mock_openweather_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OW_RESPONSE, 200))


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openweather_parsing(mock_openweather_get):
    provider = OpenWeatherWeatherProvider(WeatherConfig, Coords)
    assert isinstance(provider, OpenWeatherWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == WeatherData(
        datetime.now(timezone.utc),
        "openweather",
        298.48,  # hella hot
        64,
        "N",
        349,
        0.62,
    )


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openmeteo_parsing(mock_openmeteo_get):
    provider = OpenMeteoWeatherProvider({}, Coords)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == WeatherData(
        datetime.now(timezone.utc),
        "openmeteo",
        2.4,
        86,
        "E",
        95,
        11.9,
    )


def test_net_provider_creation():
    provider = create_net_weather_provider(WeatherConfig("openmeteo", ""), Coords)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(
        WeatherConfig("openweather", "api_key"), Coords
    )
    assert isinstance(provider, OpenWeatherWeatherProvider)
