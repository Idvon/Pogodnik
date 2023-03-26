from pytest import fixture, raises

from src.exceptions import ProviderNoDataError
from src.geo.geocoding import OpenWeatherGeoProvider
from tests.conftest import MockResponse
from tests.unit.constants import GEOCODING_ERROR_RESPONSE, GEOCODING_RESPONSE

GET_PATH = "src.geo.geocoding.get"


@fixture
def mock_geocoding_get(mocker):
    mocker.patch(GET_PATH, lambda _: MockResponse(GEOCODING_RESPONSE, 200))


@fixture
def mock_geocoding_api_error(mocker):
    mocker.patch(GET_PATH, lambda _: MockResponse(GEOCODING_ERROR_RESPONSE, 404))


@fixture
def mock_geocoding_city_not_found(mocker):
    mocker.patch(GET_PATH, lambda _: MockResponse([], 404))


def test_geocoding_parser(mock_geocoding_get):
    provider = OpenWeatherGeoProvider({"api_key": "beepboop", "city_name": "Booberg"})
    assert provider.get_city_data() == {"city": "London", "state": "", "country": "GB"}
    assert provider.get_coords() == {"lat": 51.5085, "lon": -0.1257}


def test_geocoding_city_not_found(mock_geocoding_city_not_found):
    provider = OpenWeatherGeoProvider({"api_key": "beepboop", "city_name": "Booberg"})
    with raises(ProviderNoDataError):
        provider.get_coords()


def test_geocoding_api_error(mock_geocoding_api_error):
    provider = OpenWeatherGeoProvider({"api_key": "beepboop", "city_name": "Booberg"})
    with raises(ProviderNoDataError):
        provider.get_coords()
