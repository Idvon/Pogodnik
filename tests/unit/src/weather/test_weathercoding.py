from pytest import fixture

from src.weather.weathercoding import (
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    create_net_weather_provider,
)
from tests.conftest import MockResponse
from tests.unit.constants import COORDS, OM_RESPONSE, OW_RESPONSE

GET_PATH = "src.weather.weathercoding.get"


@fixture
def mock_openmeteo_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OM_RESPONSE, 200))


@fixture
def mock_openweather_get(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse(OW_RESPONSE, 200))


def test_openweather_parsing(mock_openweather_get):
    provider = OpenWeatherWeatherProvider({"api_key": "beepboop"}, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == {
        "provider": "openweather",
        "temp": 298.48,  # hella hot
        "hum": 64,
        "winddir": "N",
        "winddeg": 349,
        "windspeed": 0.62,
    }


def test_openmeteo_parsing(mock_openmeteo_get):
    provider = OpenMeteoWeatherProvider({}, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    data = provider.weather_data(provider.request())
    assert data == {
        "provider": "openmeteo",
        "temp": 2.4,
        "hum": 86,
        "winddir": "E",
        "winddeg": 95,
        "windspeed": 11.9,
    }


def test_net_provider_creation():
    provider = create_net_weather_provider({"provider": "openmeteo"}, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(
        {"provider": "openweather", "api_key": "beepboop"}, COORDS
    )
    assert isinstance(provider, OpenWeatherWeatherProvider)
