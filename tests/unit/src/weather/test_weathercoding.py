import requests
import requests_mock
from freezegun import freeze_time

from src.weather.weathercoding import (
    DBWeatherProvider,
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    create_local_weather_provider,
    create_net_weather_provider,
)
from tests.unit.constants import (
    COORDS,
    GEO_DATA,
    LOCAL_CITY,
    LOCAL_FILE,
    LOCAL_TIMEOUT,
    OM_RESPONSE,
    OM_URL,
    OM_WEATHER_CONFIG,
    OM_WEATHER_DATA,
    OW_RESPONSE,
    OW_URL,
    OW_WEATHER_CONFIG,
    OW_WEATHER_DATA,
)

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
        assert provider.weather_data(provider.request()) == OW_WEATHER_DATA


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_openmeteo_parsing():
    provider = OpenMeteoWeatherProvider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    with requests_mock.Mocker() as m:
        m.get(OM_URL, json=OM_RESPONSE)
        assert provider.weather_data(provider.request()) == OM_WEATHER_DATA


@freeze_time("2023-01-01 00:00:00.000000+00:00")
def test_local_provider_parsing():
    provider = DBWeatherProvider(LOCAL_FILE, LOCAL_CITY, LOCAL_TIMEOUT)
    assert isinstance(provider, DBWeatherProvider)
    assert provider.weather_data(provider) == (OW_WEATHER_DATA, GEO_DATA)


def test_net_provider_creation():
    provider = create_net_weather_provider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)


def test_local_provider_creation():
    provider = create_local_weather_provider(LOCAL_FILE, LOCAL_CITY, LOCAL_TIMEOUT)
    assert isinstance(provider, DBWeatherProvider)
