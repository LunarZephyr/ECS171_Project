This sample flask app uses a stored sample regression model from
`EDA/Shreyas/price_prediction.ipynb` to make price predictions.

To run the flask server:

 - `pip install flask pickle5`
 - Run the `EDA/Shreyas/price_prediction.ipynb` notebook. It will create a
   `model_pkl` file that stores the model that is read from disk by flask.
 - `flask run` in the `www` directory