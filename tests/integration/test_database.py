from datetime import datetime, timedelta, timezone
from os import getenv
from pathlib import Path

from src.config_file_parser.file_parser import create_parser
from src.geo.geocoding import Coords, GeoData, create_geo_provider
from src.weather.weathercoding import create_net_weather_provider

# basically it's just pogodnik.py
file_config = Path("example_config.toml")
file_out = Path("out.csv")
file_db = Path("db.sqlite3")

config_parser = create_parser(file_config)
config_parser.config["geo_provider"]["api_key"] = getenv("OW_API_KEY")
config_parser.config["weather_provider"]["api_key"] = getenv("OW_API_KEY")
geo_config = config_parser.get_geo_config()
weather_config = config_parser.get_weather_config()
geo_provider = create_geo_provider(geo_config)
coords = geo_provider.get_coords()
geo_data = geo_provider.get_city_data()
net_weather_provider = create_net_weather_provider(weather_config, coords)
weather_data = net_weather_provider.weather_data(net_weather_provider.request())


def test_fetches_coords():
    assert coords == Coords(59.938732, 30.316229)
    assert geo_data == GeoData(
        city="Saint Petersburg", state="Saint Petersburg", country="RU"
    )


def test_fetches_weather():
    assert (
        -timedelta(seconds=120)
        < weather_data.datetime - datetime.now(timezone.utc)
        < timedelta(seconds=120)
    )
    assert -50 < weather_data.temp < 50
    assert 0 < weather_data.hum < 100
    for letter in weather_data.winddir:
        assert letter in ("N", "E", "S", "W")
