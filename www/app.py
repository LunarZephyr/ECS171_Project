from flask import Flask, jsonify
import pickle5 as pickle
import requests
import pandas as pd

API_KEY = "a11c32d6bed06cc334b5bcd036947fad"

app = Flask(__name__, static_url_path="", static_folder="client/build")

with open("model_pkl", "rb") as f:
    model = pickle.load(f)

min_temp = 272
max_temp = 306

min_price = 13.55
max_price = 99.5


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/prediction/current")
def get_current_prediction():
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=valencia&appid={API_KEY}"
    ).json()
    temp = weather_data["main"]["temp"]
    temp_norm = (temp - min_temp) / (max_temp - min_temp)
    price_pred = model.predict([[temp_norm]])[0]
    price_pred = price_pred * (max_price - min_price) + min_price
    return jsonify(dict(price=price_pred))
