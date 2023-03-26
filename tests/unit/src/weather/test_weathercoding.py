from src.weather.weathercoding import (
    OpenMeteoWeatherProvider,
    OpenWeatherWeatherProvider,
    create_net_weather_provider,
)
from tests.unit.src.weather.constants import COORDS, OM_RESPONSE, OW_RESPONSE


# https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
# This method will be used by the mock to replace requests.get
def mocked_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0].startswith("https://api.openweathermap.org/data/2.5/weather?"):
        return MockResponse(OW_RESPONSE, 200)
    elif args[0].startswith("https://api.open-meteo.com/v1/forecast?"):
        return MockResponse(OM_RESPONSE, 200)
    return MockResponse(None, 404)


def test_openweather_parsing(mocker):
    mocker.patch("src.weather.weathercoding.get", mocked_get)
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


def test_openmeteo_parsing(mocker):
    mocker.patch("src.weather.weathercoding.get", mocked_get)
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
