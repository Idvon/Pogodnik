from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from PoGoDnIk import get_cache, main, to_cache
from src.config_file_parser.file_parser import create_parser
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import to_display

APP = Flask(__name__)
CONFIG = Path("c.json")


def get_config():
    if not CONFIG.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(CONFIG)
    return config_parser


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    if request.method == "POST":
        city_name = request.form["city_name"]
        return redirect(url_for("response", city_name=city_name))
    return render_template("index.html")


@APP.route("/response/<city_name>")
async def response(city_name):
    geo_config = get_config().get_geo_config()
    timeout = get_config().get_timeout()
    city_name = [city_name]
    cache = get_cache(city_name, timeout)
    if type(cache[0]) is not str:
        cdata = to_display(cache[0])
        return render_template("data.html", data=cdata)
    else:
        geo_provider = create_geo_provider(geo_config, city_name[0])
        await geo_provider.request()
        city_list = geo_provider.response
        town_list = dict()
        for elem in city_list:
            town_list[
                city_list.index(elem) + 1
            ] = f"name: {elem['name']}, country: {elem['country']}, state: {elem['state']}"
        return render_template("response.html", city_list=town_list, city_name=city_name[0])


@APP.route("/data/<int:num>/<city_name>")
async def data(num: int, city_name: str):
    city_name = [city_name]
    output = Path("o.csv")
    weather_config = get_config().get_weather_config()
    geo_config = get_config().get_geo_config()
    city_data, cache_data = await main(geo_config, weather_config, city_name, num - 1)
    await to_cache(cache_data, output)
    data_template = to_display(city_data[0])
    return render_template("data.html", data=data_template)
