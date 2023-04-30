from pytest import raises

from src.exceptions import ProviderNoDataError
from src.geo.geocoding import OpenWeatherGeoProvider
from tests.unit.constants import (
    COORDS,
    GEO_CONFIG,
    GEO_DATA,
    GEOCODING_ERROR_RESPONSE,
    GEOCODING_RESPONSE,
    OW_GEO_URL,
)
import requests
import requests_mock

with requests_mock.Mocker() as m:
    m.get(OW_GEO_URL, json=GEOCODING_RESPONSE)
    requests.get(OW_GEO_URL).json()

with requests_mock.Mocker() as m:
    m.get(OW_GEO_URL, json=GEOCODING_ERROR_RESPONSE)
    requests.get(OW_GEO_URL).json()

with requests_mock.Mocker() as m:
    m.get(OW_GEO_URL, json=[])
    requests.get(OW_GEO_URL).json()


def test_geocoding_parser():
    with requests_mock.Mocker() as m:
        m.get(OW_GEO_URL, json=GEOCODING_RESPONSE)
        provider = OpenWeatherGeoProvider(GEO_CONFIG)
        geo_data = provider.get_city_data()
        assert geo_data == GEO_DATA
    assert provider.get_coords() == COORDS


def test_geocoding_city_not_found():
    provider = OpenWeatherGeoProvider(GEO_CONFIG)
    with raises(ProviderNoDataError):
        provider.get_coords()


def test_geocoding_api_error():
    provider = OpenWeatherGeoProvider(GEO_CONFIG)
    with raises(ProviderNoDataError):
        provider.get_coords()
