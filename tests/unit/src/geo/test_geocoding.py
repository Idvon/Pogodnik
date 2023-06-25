import requests
import requests_mock
from pytest import raises

from src.exceptions import ProviderNoDataError
from src.geo.geocoding import OpenWeatherGeoProvider
from tests.unit.constants import (
    COORDS,
    GEO_CONFIG,
    GEO_DATA,
    GEOCODING_ERROR_RESPONSE,
    GEOCODING_RESPONSE,
    LOCAL_CITY,
    OW_GEO_URL,
)


def test_geocoding_parser():
    with requests_mock.Mocker() as m:
        m.get(OW_GEO_URL, json=GEOCODING_RESPONSE)
        requests.get(OW_GEO_URL).json()
        provider = OpenWeatherGeoProvider(GEO_CONFIG, LOCAL_CITY)
        provider.response = GEOCODING_RESPONSE[0]
        assert provider.get_city_data() == GEO_DATA
    assert provider.get_coords() == COORDS


def test_geocoding_city_not_found():
    with requests_mock.Mocker() as m:
        m.get(OW_GEO_URL, json=GEOCODING_ERROR_RESPONSE)
        requests.get(OW_GEO_URL).json()
        provider = OpenWeatherGeoProvider(GEO_CONFIG, LOCAL_CITY)
    with raises(ProviderNoDataError):
        provider.request()


def test_geocoding_api_error():
    with requests_mock.Mocker() as m:
        m.get(OW_GEO_URL, json=[])
        requests.get(OW_GEO_URL).json()
        provider = OpenWeatherGeoProvider(GEO_CONFIG, LOCAL_CITY)
    with raises(ProviderNoDataError):
        provider.request()
