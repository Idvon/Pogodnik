from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from PoGoDnIk import get_cache, main, to_cache
from src.config_file_parser.file_parser import create_parser
from src.exceptions import ProviderNoDataError
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import to_display
from src.structures import CityData

APP = Flask(__name__)
CONFIG = Path("c.json")


# parsing config file
def get_config():
    if not CONFIG.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(CONFIG)
    return config_parser


# first page with a form to receive city name
@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    if request.method == "POST":
        city_name = request.form["city_name"]
        return redirect(url_for("response", city_name=city_name))
    return render_template("index.html")


# second page with output of city data from cache or list with selection of city from found by geo provider
@APP.route("/response/<city_name>")
async def response(city_name: str):
    geo_config = get_config().get_geo_config()
    timeout = get_config().get_timeout()
    city_name_list = [city_name]
    cache = get_cache(city_name_list, timeout)
    if type(cache[0]) is CityData:
        text = to_display(cache[0])
        return render_template("data.html", data=text)
    else:
        geo_provider = create_geo_provider(geo_config, city_name_list[0])
        await geo_provider.request()
        city_list = geo_provider.response
        town_list = dict()
        for elem in city_list:
            town_list[
                city_list.index(elem) + 1
            ] = f"name: {elem['name']}, country: {elem['country']}, state: {elem.get('state', '')}"
        return render_template(
            "response.html", city_list=town_list, city_name=city_name_list[0]
        )


# third page with output of data of selected city and writing these data to DB and output file
@APP.route("/data/<int:num>/<city_name>")
async def data(num: int, city_name: str):
    city_name_list = [city_name]
    output = Path("o.csv")
    weather_config = get_config().get_weather_config()
    geo_config = get_config().get_geo_config()
    city_data, cache_data = await main(
        geo_config, weather_config, city_name_list, num - 1
    )
    await to_cache(cache_data, output)
    data_template = to_display(city_data[0])
    return render_template("data.html", data=data_template)


# exception page
"""
@APP.route()
def parse_exception():

    return render_template("exception.html", )
"""
