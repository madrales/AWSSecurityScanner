from main import run as run_checks
from flask import Flask
from json2html import *
import json

app = Flask(__name__)

@app.route("/")


def generate():
    input = run_checks()
    x = json2html.convert(json = input, table_attributes = "id = \"mainTable\"")
    y = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/styles.css">
        <title>AWSSecurityScanner</title>
    </head>
    <body>
        <a id = "title">AWS Security Scanner</a>
        {x}
    </body>
    </html>
    """
    return y
