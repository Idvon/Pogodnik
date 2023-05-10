from flask import Flask, render_template

APP = Flask(__name__)
DATA: str


def add_data(data: str):
    global DATA
    DATA = data
    return DATA


@APP.route("/")
def web_conclusion() -> str:
    return render_template('index.html', data=add_data(DATA))
