from freezegun import freeze_time
from pytest import fixture

from src.weather.weathercoding import (
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    create_net_weather_provider,
)
from tests.conftest import MockResponse
from tests.unit.constants import (
    COORDS,
    OM_RESPONSE,
    OM_WEATHER_CONFIG,
    OM_WEATHER_DATA,
    OW_RESPONSE,
    OW_WEATHER_CONFIG,
    OW_WEATHER_DATA,
)

GET_PATH = "src.weather.weathercoding.get"


@fixture
def mock_openmeteo_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OM_RESPONSE, 200))


@fixture
def mock_openweather_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OW_RESPONSE, 200))


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openweather_parsing(mock_openweather_get):
    provider = OpenWeatherWeatherProvider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == OW_WEATHER_DATA


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openmeteo_parsing(mock_openmeteo_get):
    provider = OpenMeteoWeatherProvider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == OM_WEATHER_DATA


def test_net_provider_creation():
    provider = create_net_weather_provider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)
