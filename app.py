import asyncio
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from PoGoDnIk import get_cache, main
from src.config_file_parser.file_parser import create_parser
from src.geo.geocoding import create_geo_provider
from src.output.conclusion import to_display

APP = Flask(__name__)
CONFIG = Path("config.json")


def get_config():
    if not CONFIG.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(CONFIG)
    return config_parser


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    if request.method == "POST":
        city_name = request.form["city_name"]
        return redirect(url_for("response", city=city_name))
    return render_template("index.html")


@APP.route("/response/<city>")
def response(city):
    geo_config = get_config().get_geo_config()
    timeout = get_config().get_timeout()
    cache = get_cache(city, timeout)
    if cache:
        cdata = to_display(cache[0], cache[1])
        return render_template("data.html", data=cdata)
    else:
        geo_provider = create_geo_provider(geo_config, city)
        city_list = geo_provider.request()
        town_list = dict()
        for elem in city_list:
            town_list[
                city_list.index(elem) + 1
            ] = f"name: {elem['name']}, country: {elem['country']}, state: {elem['state']}"
        return render_template("response.html", city_list=town_list, city=city)


@APP.route("/data/<int:num>/<city>")
def data(num, city):
    output = Path("out.csv")
    weather_config = get_config().get_weather_config()
    geo_config = get_config().get_geo_config()
    weather = asyncio.run(main(geo_config, weather_config, city, output, num - 1))
    city_data = to_display(weather[0], weather[1])
    return render_template("data.html", data=city_data)
