from freezegun import freeze_time

from src.weather.weathercoding import (
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    DBWeatherProvider,
    create_net_weather_provider,
    create_local_weather_provider,
)
from tests.unit.constants import (
    COORDS,
    OM_RESPONSE,
    OM_WEATHER_CONFIG,
    OM_WEATHER_DATA,
    OM_URL,
    OW_RESPONSE,
    OW_WEATHER_CONFIG,
    OW_WEATHER_DATA,
    OW_URL,
    CACHE_CITY,
    CACHE_FILE,
    CACHE_TIMEOUT,
)
import requests
import requests_mock


with requests_mock.Mocker() as m:
    m.get(OW_URL, json=OW_RESPONSE)
    requests.get(OW_URL).json()

with requests_mock.Mocker() as m:
    m.get(OM_URL, json=OM_RESPONSE)
    requests.get(OM_URL).json()


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openweather_parsing():
    provider = OpenWeatherWeatherProvider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)
    with requests_mock.Mocker() as m:
        m.get(OW_URL, json=OW_RESPONSE)
        data = provider.weather_data(provider.request())
        assert data == OW_WEATHER_DATA


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openmeteo_parsing():
    provider = OpenMeteoWeatherProvider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    with requests_mock.Mocker() as m:
        m.get(OM_URL, json=OM_RESPONSE)
        data = provider.weather_data(provider.request())
        assert data == OM_WEATHER_DATA


def test_net_provider_creation():
    provider = create_net_weather_provider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)


def test_local_provider_creation():
    provider = create_local_weather_provider(CACHE_FILE, CACHE_CITY, CACHE_TIMEOUT)
    assert isinstance(provider, DBWeatherProvider)
