from unittest.mock import patch

import requests
import requests_mock
from freezegun import freeze_time

from src.weather.weathercoding import (
    DBWeatherProvider,
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
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


def test_net_provider_creation():
    provider = create_net_weather_provider(OM_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenMeteoWeatherProvider)
    provider = create_net_weather_provider(OW_WEATHER_CONFIG, COORDS)
    assert isinstance(provider, OpenWeatherWeatherProvider)


@freeze_time("2023-01-01 00:00:00.000000+00:00")
@patch("src.weather.weathercoding.sqlite3")
def test_db_weather_provider(mocked_connect):
    mc = mocked_connect.connect().cursor().fetchall
    mc.return_value = [
        (
            "2023-01-01 00:00:00.000000+00:00",
            "openweather",
            298.48,
            64,
            "N",
            349,
            0.62,
            "London",
            "GB",
            "",
        )
    ]
    provider = DBWeatherProvider(LOCAL_FILE, LOCAL_CITY, LOCAL_TIMEOUT)
    data = provider.weather_data()
    assert data == (OW_WEATHER_DATA, GEO_DATA)
