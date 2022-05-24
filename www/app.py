from flask import Flask, jsonify
import pickle5 as pickle
import requests
import pandas as pd
from entsoe import EntsoePandasClient
from datetime import datetime, time, timedelta
import numpy as np

OPENWEATHER_API_KEY = "a11c32d6bed06cc334b5bcd036947fad"
ENTSOE_API_KEY = "2d4af50f-d03b-435e-be11-23a69f79cb16"

app = Flask(__name__, static_url_path="", static_folder="client/build")

entsoe_client = EntsoePandasClient(api_key=ENTSOE_API_KEY)

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

weather_params = [
    "Clear",
    "Clouds",
    "Drizzle",
    "Dust",
    "Dog",
    "Haze",
    "Mist",
    "Rain",
    "Smoke",
    "Snow",
    "Squall",
    "Thunderstorm",
]

weather_features += weather_params

cities = ["valencia", "barcelona", "bilbao", "madrid", "seville"]

min_price = 13.55
max_price = 99.5


def get_one_hot_encoding_weather_main(weather_main):
    # One hot encoding of weather_main param
    # Source: https://www.educative.io/edpresso/one-hot-encoding-in-python
    mapping = {}
    for param in range(len(weather_params)):
        mapping[weather_params[param]] = param

    one_hot_encoding = []

    encoding = list(np.zeros(len(weather_params), dtype=int))
    encoding[mapping[weather_main]] = 1
    one_hot_encoding.append(encoding)

    return one_hot_encoding


def get_weather_features_data(weather_data) -> list:
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
    weather_main = get_one_hot_encoding_weather_main(
        weather_data["weather"][0]["main"]
    )[0]
    weather_features_data.extend(weather_main)

    weather_features_data_pd = pd.DataFrame(
        [weather_features_data], columns=weather_features
    )

    return weather_features_data


def get_avg_weather_features_data():
    avg_weather_data = [0] * len(weather_features)
    for city in cities:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        ).json()
        weather_data = get_weather_features_data(weather_data=weather_data)
        for i, data in enumerate(weather_data):
            avg_weather_data[i] += data
    avg_weather_data = [i / 5 for i in avg_weather_data]
    return avg_weather_data


def get_current_generation_data() -> pd.DataFrame:
    today_time = datetime.combine(datetime.today(), time.min)
    tomorrow_time = today_time + timedelta(days=1)
    generation_data: pd.DataFrame = entsoe_client.query_installed_generation_capacity(
        "ES",
        start=pd.Timestamp(today_time, tz="Europe/Madrid"),
        end=pd.Timestamp(tomorrow_time, tz="Europe/Madrid"),
    )
    day_ahead_data: pd.DataFrame = entsoe_client.query_wind_and_solar_forecast(
        "ES",
        start=pd.Timestamp(today_time, tz="Europe/Madrid"),
        end=pd.Timestamp(tomorrow_time, tz="Europe/Madrid"),
    )
    avg_day_ahead_data = pd.DataFrame(
        columns=["forecast solar day ahead", "forecast wind onshore day ahead"]
    )
    avg_day_ahead_data["forecast solar day ahead"] = [day_ahead_data["Solar"].mean()]
    avg_day_ahead_data["forecast wind onshore day ahead"] = [
        day_ahead_data["Wind Onshore"].mean()
    ]

    generation_data = pd.concat([generation_data, avg_day_ahead_data])
    return generation_data


@app.route("/prediction/current")
def get_current_prediction():
    weather_data = get_avg_weather_features_data()

    generation_data = get_current_generation_data()
    generation_data = generation_data.iloc[0].values

    price_pred = model.predict([weather_data])[0]
    price_pred = price_pred * (max_price - min_price) + min_price
    return jsonify(dict(price=price_pred))
