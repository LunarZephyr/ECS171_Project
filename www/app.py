import enum
from flask import Flask, jsonify, request, Response
import pickle5 as pickle
import requests
import pandas as pd
from entsoe import EntsoePandasClient
from datetime import datetime, time, timedelta
import numpy as np
from statistics import mode

OPENWEATHER_API_KEY = "a11c32d6bed06cc334b5bcd036947fad"
ENTSOE_API_KEY = "2d4af50f-d03b-435e-be11-23a69f79cb16"

app = Flask(__name__, static_url_path="", static_folder="client/build")

entsoe_client = EntsoePandasClient(api_key=ENTSOE_API_KEY)

with open("XGBOOST_predict_price.pkl", "rb") as f:
    model = pickle.load(f)

numerical_weather_features = [
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
    "Fog",
    "Mist",
    "Rain"
]

seasons = ["fall", "spring", "summer", "winter"]

times_of_day = ["day", "morning", "night"]

categorical_features = [weather_main_params, seasons, times_of_day]

weather_categorical_input_params = [
    "weather_main",
    "season",
    "time_of_day",
]

weather_input_params = numerical_weather_features + weather_categorical_input_params

generation_input_params = [
    "biomass",
    "fossil_brown_coal/lignite",
    "fossil_gas",
    "fossil_hard_coal",
    "fossil_oil",
    "hydro_pumped_storage_consumption",
    "hydro_run_of_river_poundage",
    "hydro_water_reservoir",
    "nuclear",
    "other",
    "other_renewable",
    "solar",
    "waste",
    "wind_onshore",
    "total_load_actual",
]

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


def get_api_numerical_weather_features_data(weather_data) -> list:
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
    return weather_features_data


def get_api_categorical_weather_features_data(weather_data) -> list:
    categorical_weather_features_data = []
    categorical_weather_features_data.append(weather_data["weather"][0]["main"])
    categorical_weather_features_data.append(get_current_season())
    categorical_weather_features_data.append(get_current_time_of_day())
    return categorical_weather_features_data


def get_avg_weather_features_data() -> pd.DataFrame:
    """
    Get the average weather feature data for the 5 cities in Spain.

    Returns:
        pd.DataFrame: A pandas Dataframe containing the averaged weather feature
        data.
    """
    avg_weather_data = [0] * len(numerical_weather_features)
    categorical_weather_data_aggr = []
    for city in cities:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
        ).json()
        numerical_weather_data = get_api_numerical_weather_features_data(
            weather_data=weather_data
        )
        categorical_weather_data = get_api_categorical_weather_features_data(
            weather_data=weather_data
        )
        categorical_weather_data_aggr.append(categorical_weather_data)
        for i, data in enumerate(numerical_weather_data):
            avg_weather_data[i] += data
    avg_weather_data = [i / 5 for i in avg_weather_data]

    # Get value of categorical features with highest frequency
    for i in range(len(categorical_weather_data_aggr[0])):
        categorical_feature_mode = mode(
            [
                categorical_weather_data_aggr[j][i]
                for j in range(len(categorical_weather_data_aggr))
            ]
        )
        avg_weather_data.extend(
            get_feature_one_hot_encoding(
                feature=categorical_feature_mode, feature_params=categorical_features[i]
            )[0]
        )
    avg_weather_data = pd.DataFrame(
        [avg_weather_data],
        columns=numerical_weather_features
        + weather_main_params
        + seasons
        + times_of_day,
    )
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
            "Wind Offshore"
        ],
        inplace=True,
    )
    total_load: pd.DataFrame = entsoe_client.query_load(
        "ES",
        start=pd.Timestamp(today_time, tz="Europe/Madrid"),
        end=pd.Timestamp(tomorrow_time, tz="Europe/Madrid"),
    )
    avg_total_load = pd.DataFrame(
        columns=["total load actual"]
    )
    avg_total_load["total load actual"] = [total_load["Actual Load"].mean()]
    generation_data = pd.concat([generation_data, avg_total_load])
    return generation_data


@app.route("/prediction/current")
def get_current_prediction():
    weather_data = get_avg_weather_features_data()
    generation_data = get_current_generation_data()
    weather_and_generation_data = pd.concat([weather_data, generation_data])

    price_pred = model.predict(weather_and_generation_data.to_numpy())[0]
    return jsonify(dict(price=str(price_pred)))


@app.route("/prediction")
def get_prediction_from_input_params():
    request_args = request.args.to_dict()

    weather_data = []
    generation_data = []
    for feature in numerical_weather_features:
        if request_args.get(feature) == None:
            return Response(
                f"{feature} feature not included in request parameters", status=400
            )
        weather_data.append(float(request_args.get(feature)))

    for i, feature in enumerate(weather_categorical_input_params):
        if request_args.get(feature) == None:
            return Response(
                f"{feature} feature not included in request parameters", status=400
            )
        categorical_feature = request_args.get(feature)
        weather_data.extend(
            get_feature_one_hot_encoding(
                feature=categorical_feature, feature_params=categorical_features[i]
            )[0]
        )

    for feature in generation_input_params:
        if request_args.get(feature) == None:
            return Response(
                f"{feature} feature not included in request parameters", status=400
            )
        generation_data.append(float(request_args.get(feature)))
    price_pred = model.predict(weather_data.to_numpy())[0]
    price_pred = price_pred * (max_price - min_price) + min_price
    return jsonify(dict(price=price_pred))
