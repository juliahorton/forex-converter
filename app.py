"""Flask application to convert one currency to another using exchangerate.host API"""

from os import getenv
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from currency_code_validation import valid_codes
import requests

app = Flask(__name__)

# find and load .env file containing Flask secret key and API access key
load_dotenv(find_dotenv())

# access environment variable to set Flask secret key
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

# access environment variable to set API access key
access_key = getenv('ACCESS_KEY')

debug = DebugToolbarExtension(app)

@app.route('/')
def index():
    """Display home page"""
    return render_template("index.html")


@app.route('/convert')
def call_api():
    """Make a call to the forex converter API and display the result of currency conversion"""

    # ensure that "convert from" currency is valid
    curr_from = request.args["convert-from"].upper()

    if (curr_from not in valid_codes):
        msg = f"Not a valid code: {curr_from}"
        return render_template("index.html",msg=msg, alert_status="danger")

    # ensure that "convert to" currency is valid
    curr_to = request.args["convert-to"].upper()

    if (curr_to not in valid_codes):
        msg = f"Not a valid code: {curr_to}"
        return render_template("index.html",msg=msg, alert_status="danger")

    # ensure that amount to convert is a valid number
    amt = request.args["amount"]

    try: 
        amt = float(amt)
    except:
        msg = "Not a valid amount."
        return render_template("index.html",msg=msg, alert_status="danger")
    
    if (amt <= 0):
        msg = "Not a valid amount."
        return render_template("index.html",msg=msg, alert_status="danger")
    
    # make a call to the currency converter API
    api_response = requests.get(f"http://api.exchangerate.host/convert?access_key={access_key}&from={curr_from}&to={curr_to}&amount={amt}").json()
    
    # save result of conversion, rounded to two decimal places
    result = round(api_response["result"],2)

    # display result of currency conversion
    msg = f"The result is {result} {curr_to}."

    return render_template("index.html",msg=msg, alert_status="success", curr_from=curr_from, curr_to=curr_to, amt=amt)
