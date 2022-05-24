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

weather_main_params = [
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

seasons = ["fall", "spring", "summer", "winter"]

times_of_day = ["day", "morning", "night"]
# weather_features += weather_main_params

cities = ["valencia", "barcelona", "bilbao", "madrid", "seville"]

min_price = 13.55
max_price = 99.5


def get_feature_one_hot_encoding(feature, feature_params):
    """
    Generate One-hot Encoding of a feature
    Source: https://www.educative.io/edpresso/one-hot-encoding-in-python

    Args:
        feature: Feature value to encode
        feature_params: All possible values of the feature

    Returns:
        list: One-hot encoding of the feature value
    """
    mapping = {}
    for param in range(len(feature_params)):
        mapping[feature_params[param]] = param

    one_hot_encoding = []

    encoding = list(np.zeros(len(feature_params), dtype=int))
    encoding[mapping[feature]] = 1
    one_hot_encoding.append(encoding)

    return one_hot_encoding


def get_current_time_of_day():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hour = int(current_time[11:13])
    if hour >= 6 and hour < 12:
        return "morning"
    elif hour >= 12 and hour <= 17:
        return "day"
    return "night"


def get_current_season():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    month = int(current_time[5:7])

    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"


def get_api_weather_features_data(weather_data) -> list:
    """
    Get the current values of all the weather features from the JSON file
    returned by the OpenWeather API.

    Args:
        weather_data: dictionary containing the weather data returned by the
        API.

    Returns:
        list: List of the weather feature values
    """
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
        if weather_data["rain"].get("1h"):
            weather_features_data.append(weather_data["rain"]["1h"])
        else:
            weather_features_data.append(0)
        if weather_data["rain"].get("3h"):
            weather_features_data.append(weather_data["rain"]["3h"])
        else:
            weather_features_data.append(0)
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
    weather_main = get_feature_one_hot_encoding(
        feature=weather_data["weather"][0]["main"], feature_params=weather_main_params
    )[0]
    # weather_features_data.extend(weather_main)
    time_of_day = get_feature_one_hot_encoding(
        feature=get_current_time_of_day(), feature_params=times_of_day
    )[0]
    current_season = get_feature_one_hot_encoding(
        feature=get_current_season(), feature_params=seasons
    )[0]
    print(time_of_day, current_season)

    return weather_features_data


def get_avg_weather_features_data() -> pd.DataFrame:
    """
    Get the average weather feature data for the 5 cities in Spain.

    Returns:
        pd.DataFrame: A pandas Dataframe containing the averaged weather feature
        data.
    """
    avg_weather_data = [0] * len(weather_features)
    for city in cities:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        ).json()
        weather_data = get_api_weather_features_data(weather_data=weather_data)
        for i, data in enumerate(weather_data):
            avg_weather_data[i] += data
    avg_weather_data = [i / 5 for i in avg_weather_data]
    avg_weather_data = pd.DataFrame([avg_weather_data], columns=weather_features)
    return avg_weather_data


def get_current_generation_data() -> pd.DataFrame:
    """
    Extract the current generation data from the ENTSOE API.

    Returns:
        pd.DataFrame: Pandas Dataframe containing current generation data
    """
    today_time = datetime.combine(datetime.today(), time.min)
    tomorrow_time = today_time + timedelta(days=1)
    generation_data: pd.DataFrame = entsoe_client.query_installed_generation_capacity(
        "ES",
        start=pd.Timestamp(today_time, tz="Europe/Madrid"),
        end=pd.Timestamp(tomorrow_time, tz="Europe/Madrid"),
    )
    generation_data.drop(
        columns=[
            "Geothermal",
            "Fossil Peat",
            "Fossil Oil shale",
            "Fossil Coal-derived gas",
            "Marine",
        ],
        inplace=True,
    )
    day_ahead_data: pd.DataFrame = entsoe_client.query_wind_and_solar_forecast(
        "ES",
        start=pd.Timestamp(tomorrow_time, tz="Europe/Madrid"),
        end=pd.Timestamp(tomorrow_time + timedelta(days=1), tz="Europe/Madrid"),
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
    print(generation_data.columns)
    generation_data = generation_data.iloc[0].values

    price_pred = model.predict(weather_data.to_numpy())[0]
    price_pred = price_pred * (max_price - min_price) + min_price
    return jsonify(dict(price=price_pred))
