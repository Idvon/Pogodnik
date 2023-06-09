import json
from os import getenv
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for
from wtforms import Form, StringField

from PoGoDnIk import get_city_geo_data, get_city_list, get_config, main, parser_files

APP = Flask(__name__)


class MyForm(Form):
    city_name = StringField("City Name")
    num_city = StringField("Number of City")


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    form = MyForm(request.form)
    file_config = Path(getenv("FILE_CONFIG"))
    with open(file_config) as f:
        config_data = json.load(f)
    file_output = Path(getenv("FILE_OUTPUT"))
    if request.method == "POST":
        city_name = request.form.get("city_name")
        config_data["city_name"] = city_name
        file_config = Path("net_config.json")
        with open(file_config, "w") as f:
            json.dump(config_data, f)
        parser_files(file_config, file_output)
        return redirect(url_for("response"))
    return render_template("index.html", city_name=form)


@APP.route("/response", methods=["GET", "POST"])
def response():
    get_config()
    city_list = get_city_list()
    return render_template("response.html", city_list=city_list)


@APP.route("/data/<int:num>")
def data(num):
    get_city_geo_data(num - 1)
    return render_template("data.html", data=main())
