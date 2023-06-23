from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from PoGoDnIk import main, get_cache
from src.config_file_parser.file_parser import create_parser
from src.geo.geocoding import create_geo_provider

APP = Flask(__name__)


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    if request.method == "POST":
        city_name = request.form['city_name']
        return redirect(url_for("response", city=city_name))
    return render_template("index.html")


@APP.route("/response/<city>")
def response(city):
    file_db = Path("db.sqlite3")
    config = Path("config.json")
    if not config.is_file():
        raise FileNotFoundError("Config file not found")
    config_parser = create_parser(config)
    geo_config = config_parser.get_geo_config()
    weather_config = config_parser.get_weather_config()
    timeout = config_parser.get_timeout()
    cache = get_cache(city, timeout, file_db)
    if cache:
        return redirect(url_for("data", city=cache))
    else:
        geo_provider = create_geo_provider(geo_config, city)
        city_list = geo_provider.request()
        town_list = dict()
        for city in city_list:
            town_list[
                city_list.index(city) + 1
                ] = f"name: {city['name']}, country: {city['country']}, state: {city['state']}"
    return render_template("response.html", city_list=town_list)


@APP.route("/data/<int:num>")
def data(num):
    output = Path("out.csv")
    file_db = Path("db.sqlite3")
    return render_template(
        "data.html",
        data=main(weather_config, output, file_db))
