from flask import Flask, render_template
from os import getenv
from PoGoDnIk import *

APP = Flask(__name__)


@APP.route("/")
def web_conclusion() -> str:
    file_config = Path(getenv("FILE_CONFIG"))
    file_output = Path(getenv("FILE_OUTPUT"))
    return render_template("index.html", data=main(file_config, file_output))
