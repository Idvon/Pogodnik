from datetime import datetime, timezone
from pathlib import Path

from freezegun import freeze_time

from src.structures import Coords, GeoConfig, GeoData, WeatherConfig, WeatherData

FREEZER = freeze_time("2023-01-01 00:00:00.000000+00:00")
GEO_CONFIG = GeoConfig("London", "provider", "api_key")
GEO_DATA = GeoData("London", "", "GB")
COORDS = Coords(51.5085, -0.1257)

OW_WEATHER_CONFIG = WeatherConfig("openweather", "api_key")
OW_URL = "https://api.openweathermap.org/data/2.5/weather"
OW_GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
OM_WEATHER_CONFIG = WeatherConfig("openmeteo", "")
OM_URL = "https://api.open-meteo.com/v1/forecast"

LOCAL_FILE = Path("db.sqlite3")
LOCAL_CITY = "London"
LOCAL_TIMEOUT = 1

FREEZER.start()
OW_WEATHER_DATA = WeatherData(
    datetime.now(timezone.utc),
    "openweather",
    298.48,  # hella hot
    64,
    "N",
    349,
    0.62,
)
OM_WEATHER_DATA = WeatherData(
    datetime.now(timezone.utc),
    "openmeteo",
    2.4,
    86,
    "E",
    95,
    11.9,
)
FREEZER.stop()

OW_RESPONSE = {
    "coord": {"lon": 10.99, "lat": 44.34},
    "weather": [
        {
            "id": 501,
            "main": "Rain",
            "description": "moderate rain",
            "icon": "10d",
        }
    ],
    "base": "stations",
    "main": {
        "temp": 298.48,
        "feels_like": 298.74,
        "temp_min": 297.56,
        "temp_max": 300.05,
        "pressure": 1015,
        "humidity": 64,
        "sea_level": 1015,
        "grnd_level": 933,
    },
    "visibility": 10000,
    "wind": {"speed": 0.62, "deg": 349, "gust": 1.18},
    "rain": {"1h": 3.16},
    "clouds": {"all": 100},
    "dt": 1661870592,
    "sys": {
        "type": 2,
        "id": 2075663,
        "country": "IT",
        "sunrise": 1661834187,
        "sunset": 1661882248,
    },
    "timezone": 7200,
    "id": 3163858,
    "name": "Zocca",
    "cod": 200,
}

OM_RESPONSE = {
    "current_weather": {
        "time": "2022-01-01T02:00",
        "temperature": 2.4,
        "weathercode": 3,
        "windspeed": 11.9,
        "winddirection": 95.0,
    },
    "hourly": {
        "time": ["2022-01-01T00:00", "2022-01-01T01:00", "2022-01-01T02:00"],
        "windspeed_10m": [3.16, 3.02, 3.3],
        "temperature_2m": [13.7, 13.3, 12.8],
        "relativehumidity_2m": [82, 83, 86],
    },
}
GEOCODING_RESPONSE = [
    {
        "name": "London",
        "local_names": {
            # bla bla
        },
        "lat": 51.5085,
        "lon": -0.1257,
        "country": "GB",
    },
    {
        "name": "London",
        "local_names": {
            # bla bla
        },
        "lat": 42.9834,
        "lon": -81.233,
        "country": "CA",
    },
]
GEOCODING_ERROR_RESPONSE = {"cod": 429}
