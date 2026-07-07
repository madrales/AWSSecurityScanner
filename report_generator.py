from main import run as run_checks
from flask import Flask
from json2html import *
import json

app = Flask(__name__)

@app.route("/")


def generate():
    input = run_checks()
    return json2html.convert(json = input)
