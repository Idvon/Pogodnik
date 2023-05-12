from os import getenv
from pathlib import Path

from flask import Flask, render_template

from PoGoDnIk import parser_files

APP = Flask(__name__)


@APP.route("/")
def web_conclusion():
    file_config = Path(getenv("FILE_CONFIG"))
    file_output = Path(getenv("FILE_OUTPUT"))
    city_data = parser_files(file_config, file_output)
    return render_template("index.html", data=city_data)
