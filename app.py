import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

from PoGoDnIk import get_city_geo_data, get_city_list, get_config, main

APP = Flask(__name__)


class MyForm(Form):
    city_name = StringField("City Name")


def get_net_config(city_name: str):
    file_config = Path("config.json")
    with open(file_config) as f:
        config_data = json.load(f)
    config_data["city_name"] = city_name
    file_config = Path("net_config.json")
    with open(file_config, "w") as f:
        json.dump(config_data, f)


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    form = MyForm(request.form)
    if request.method == "POST":
        city_name = request.form.get("city_name")
        get_net_config(city_name)
        return redirect(url_for("response"))
    return render_template("index.html", city_name=form)


@APP.route("/response", methods=["GET", "POST"])
def response():
    file_config = Path("net_config.json")
    geo_config, weather_config, timeout = get_config(file_config)
    geo_provider, city_list = get_city_list(geo_config)
    return render_template("response.html", city_list=city_list)


@APP.route("/data/<int:num>")
def data(num):
    file_output = Path("out.csv")
    file_config = Path("net_config.json")
    geo_config, weather_config, timeout = get_config(file_config)
    geo_provider, city_list = get_city_list(geo_config)
    coords, city_geo_data = get_city_geo_data(geo_provider, num - 1)
    return render_template(
        "data.html",
        data=main(
            geo_config, weather_config, coords, city_geo_data, file_output, timeout
        ),
    )
