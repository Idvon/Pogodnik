import json
from os import getenv
from pathlib import Path

from flask import Flask, render_template, request
from wtforms import Form, StringField
from PoGoDnIk import parser_files

APP = Flask(__name__)


class MyForm(Form):
    city_name = StringField('City Name')


@APP.route("/", methods=["GET", "POST"])
def web_conclusion():
    form = MyForm(request.form)
    file_config = Path(getenv("FILE_CONFIG"))
    with open(file_config) as f:
        confit_data = json.load(f)
    file_output = Path(getenv("FILE_OUTPUT"))
    if request.method == "POST":
        city_name = request.form.get('city_name')
        confit_data['city_name'] = city_name
        file_config = Path("net_config.json")
        with open(file_config, "a") as f:
            json.dump(confit_data, f)
        return render_template("data.html", data=parser_files(file_config, file_output))
    return render_template("index.html", city_name=form)
