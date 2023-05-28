from os import getenv
from pathlib import Path

from flask import Flask, render_template
from wtforms import Form, StringField, validators
from PoGoDnIk import parser_files

APP = Flask(__name__)


class MyForm(Form):
    first = StringField('City Name', [validators.Length(min=3, max=30)])


@APP.route("/")
def web_conclusion():
    file_config = Path(getenv("FILE_CONFIG"))
    file_output = Path(getenv("FILE_OUTPUT"))
    city_config = parser_files(file_config, file_output)    # sending work files
    return render_template("index.html", data=city_config)
