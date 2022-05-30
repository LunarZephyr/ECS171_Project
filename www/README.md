This flask app uses the XGBoost model located in `EDA/Jacqueline`. 

To run the flask server:

 - `pip install -r requirements.txt`
 - Copy the `XGBOOST_predict_price.pkl` file into the `www` directory.
 - `flask run --reload` in the `www` directory

Currently, there are 2 API endpoints: 
- `/prediction/current` for predicting price based on current weather and
  generation data
- `/prediction` for predicting price based on user inputs.

When making a request to the `/prediction` endpoint from the frontend, the
request params for the user inputted values should follow the following names:

`["temp", "pressure", "humidity", "wind_speed", "wind_deg", "rain_1h",
    "rain_3h", "snow_3h", "clouds_all", "weather_main", "season", "time_of_day",
    "biomass", "fossil_brown_coal/lignite", "fossil_gas", "fossil_hard_coal",
    "fossil_oil", "hydro_pumped_storage_consumption",
    "hydro_run_of_river_poundage", "hydro_water_reservoir", "nuclear", "other",
    "other_renewable", "solar", "waste", "wind_onshore", "total_load_actual"]`

For the categorical weather attributes when sending user input to the backend:
 - `weather_main` should have one of the following values: `["Clear", "Clouds",
  "Drizzle", "Fog", "Mist", "Rain"]`
 - `season` should be one of the following: `["fall", "spring", "summer", "winter"]`
 - `time_of_day` should be one of the following: `["day", "morning", "night"]`