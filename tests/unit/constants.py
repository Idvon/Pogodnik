from datetime import datetime, timezone
from pathlib import Path

from freezegun import freeze_time

from src.structures import (
    CityData,
    Coords,
    GeoConfig,
    GeoData,
    WeatherConfig,
    WeatherData,
)

GEO_CONFIG = GeoConfig("provider", 2, "api_key")
GEO_DATA = GeoData("London", "GB", "England")
COORDS = Coords(51.5085, -0.1257)

OW_WEATHER_CONFIG = WeatherConfig("openweather", "api_key")
OW_URL = "https://api.openweathermap.org/data/2.5/weather"
OW_GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
OM_WEATHER_CONFIG = WeatherConfig("openmeteo", "")
OM_URL = "https://api.open-meteo.com/v1/forecast"

LOCAL_FILE = Path("db.sqlite3")
LOCAL_CITY = "London"

TIMEOUT = 0

with freeze_time("2023-01-01 00:00:00.000000+00:00"):
    OW_WEATHER_DATA = WeatherData(
        datetime.now(timezone.utc),
        "openweather",
        "Rain",
        298.74,  # hella hot
        64,
        "N",
        349,
        0.62,
        100,
        3.16,
        3163858,
    )
    OM_WEATHER_DATA = WeatherData(
        datetime.now(timezone.utc),
        "openmeteo",
        "Clouds",
        11.5,
        76,
        "NE",
        30,
        2.2,
        76,
        0.0,
        None,
    )
    OW_CITY_DATA = CityData(OW_WEATHER_DATA, GEO_DATA)
    OM_CITY_DATA = CityData(OM_WEATHER_DATA, GEO_DATA)
    LIST_CITY_DATA = [OW_CITY_DATA, OM_CITY_DATA]

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
    "latitude": 51.5,
    "longitude": -0.120000124,
    "generationtime_ms": 0.07534027099609375,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "timezone_abbreviation": "GMT",
    "elevation": 1.0,
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "apparent_temperature": "°C",
        "relative_humidity_2m": "%",
        "wind_direction_10m": "°",
        "wind_speed_10m": "m/s",
        "precipitation": "mm",
        "cloud_cover": "%",
        "rain": "mm",
        "showers": "mm",
        "snowfall": "cm",
    },
    "current": {
        "time": "2025-08-14T17:15",
        "interval": 900,
        "apparent_temperature": 11.5,
        "relative_humidity_2m": 76,
        "wind_direction_10m": 30,
        "wind_speed_10m": 2.20,
        "precipitation": 0.00,
        "cloud_cover": 76,
        "rain": 0.00,
        "showers": 0.00,
        "snowfall": 0.00,
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
        "state": "England",
    },
    {
        "name": "London",
        "local_names": {
            # bla bla
        },
        "lat": 42.9834,
        "lon": -81.233,
        "country": "CA",
        "state": "Ontario",
    },
]
GEOCODING_ERROR_RESPONSE = {"cod": 401, "message": "Invalid"}
