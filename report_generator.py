from main import run as run_checks
from flask import Flask
from json2html import *
from htmlize import htmlConvert

import json

app = Flask(__name__)

@app.route("/")


def generate():
    input = run_checks()

    generated_at = htmlConvert(input["generated_at"], "summary")
    account_id = htmlConvert(input["account_id"], "summary")
    summary = htmlConvert(input["summary"], "summary")
    high = htmlConvert(input["high_violations"], "high")
    med = htmlConvert(input["med_violations"], "med")
    low = htmlConvert(input["low_violations"], "low")
    
    bodyHTML = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/styles.css">
        <title>AWSSecurityScanner</title>
    </head>
    <body>
        <a id = "title">AWS Security Scanner</a>
        <div class="summary-card">
            <div class="summary-row">
                <span class="label">GENERATED_AT:</span> <span class="value">{generated_at}</span>
            </div>
            <div class="summary-row">
                <span class="label">ACCOUNT_ID:</span> <span class="value">{account_id}</span>        
            </div>
            <div class="summary-row">
                <span class="label">VIOLATION_SUMMARY</span> <span class="value">{summary}</span>           
            </div>
        </div>
        {high}
        {med}
        {low}
    </body>
    </html>
    """
    return bodyHTML