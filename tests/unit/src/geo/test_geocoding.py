from pytest import fixture, raises

from src.exceptions import ProviderNoDataError
from src.geo.geocoding import OpenWeatherGeoProvider
from tests.conftest import MockResponse
from tests.unit.constants import (
    COORDS,
    GEO_CONFIG,
    GEO_DATA,
    GEOCODING_ERROR_RESPONSE,
    GEOCODING_RESPONSE,
)

GET_PATH = "src.geo.geocoding.get"


@fixture
def mock_geocoding_get(mocker):
    mocker.patch(
        GET_PATH, lambda *args, **kwargs: MockResponse(GEOCODING_RESPONSE, 200)
    )


@fixture
def mock_geocoding_api_error(mocker):
    mocker.patch(
        GET_PATH, lambda *args, **kwargs: MockResponse(GEOCODING_ERROR_RESPONSE, 404)
    )


@fixture
def mock_geocoding_city_not_found(mocker):
    mocker.patch(GET_PATH, lambda *args, **kwargs: MockResponse([], 404))


def test_geocoding_parser(mock_geocoding_get):
    provider = OpenWeatherGeoProvider(GEO_CONFIG)
    assert provider.get_city_data() == GEO_DATA
    assert provider.get_coords() == COORDS


def test_geocoding_city_not_found(mock_geocoding_city_not_found):
    provider = OpenWeatherGeoProvider(GEO_CONFIG)
    with raises(ProviderNoDataError):
        provider.get_coords()


def test_geocoding_api_error(mock_geocoding_api_error):
    provider = OpenWeatherGeoProvider(GEO_CONFIG)
    with raises(ProviderNoDataError):
        provider.get_coords()
