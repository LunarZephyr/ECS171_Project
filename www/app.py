from flask import Flask, jsonify
import pickle5 as pickle
import requests
import pandas as pd

API_KEY = "a11c32d6bed06cc334b5bcd036947fad"

app = Flask(__name__, static_url_path="", static_folder="client/build")

with open("model_pkl", "rb") as f:
    model = pickle.load(f)

weather_features = [
    "temp",
    "pressure",
    "humidity",
    "wind_speed",
    "wind_deg",
    "rain_1h",
    "rain_3h",
    "snow_3h",
    "clouds_all",
]

weather_min_max_values = dict(
    temp=[272, 306],
    pressure=[812, 202469],
    humidity=[26.6, 98.6],
    wind_speed=[0.2, 28.8],
    wind_deg=[0.0, 334.8],
    rain_1h=[0.0, 3.06],
    rain_3h=[0.0, 0.463],
    snow_3h=[0.0, 4.3],
    clouds_all=[0.0, 92.0],
)

min_temp = 272
max_temp = 306

min_price = 13.55
max_price = 99.5


def get_weather_features_data(weather_data):
    weather_features_data = []
    weather_features_data.extend(
        [
            weather_data["main"]["temp"],
            weather_data["main"]["pressure"],
            weather_data["main"]["humidity"],
        ]
    )
    weather_features_data.extend(
        [weather_data["wind"]["speed"], weather_data["wind"]["deg"]]
    )
    if weather_data.get("rain"):
        weather_features_data.extend(
            [weather_data["rain"]["1h"], weather_data["rain"]["3h"]]
        )
    else:
        weather_features_data.extend([0, 0])
    if weather_data.get("snow"):
        weather_features_data.append(weather_data["snow"]["3h"])
    else:
        weather_features_data.append(0)
    if weather_data.get("clouds"):
        weather_features_data.append(weather_data["clouds"]["all"])
    else:
        weather_features_data.append(0)
    return weather_features_data


def normalize_weather_data(weather_data):
    weather_features_data = get_weather_features_data(weather_data=weather_data)

    for i in range(len(weather_features_data)):
        min_val, max_val = (
            weather_min_max_values[weather_features[i]][0],
            weather_min_max_values[weather_features[i]][1],
        )
        weather_features_data[i] = (weather_features_data[i] - min_val) / (
            max_val - min_val
        )

    return weather_features_data


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/prediction/current")
def get_current_prediction():
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=valencia&appid={API_KEY}"
    ).json()
    weather_data = normalize_weather_data(weather_data=weather_data)
    price_pred = model.predict([weather_data])[0]
    price_pred = price_pred * (max_price - min_price) + min_price
    return jsonify(dict(price=price_pred))
