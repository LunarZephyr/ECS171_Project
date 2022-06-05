# ECS171 Group 25 Final Project

The Github repo has the following structure:

- The `data` folder contains the raw csv files from our
  [dataset](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather).
- The `EDA` folder contains exploratory data analysis performed by each team member
  on the csv files.
  - The `EDA/Ameya` folder contains the source code for our NN model.
  - The `Models_XGBoost_and_SHAP.ipynb` folder contains the source code for our XGBoost model for price prediction and the SHAP analysis.
- The data-wrangling and data-engineering notebook `Dataset_Engineering_Preparation.ipynb` contains feature engineering and preparing a baseline training and testing for ou rmodel
  - The resulting data file from running this notebook that is used to train the models is called `final_baseline_data.csv`
- The source code for the models can also be found in the `Models.ipynb` and
  `Models.py` files.
- The `Report` folder contains the tex file of our final report along with the
  images used.
- The `www` folder contains the source code of
  our project website.
  - Instructions on running the flask back-end and interacting with the web
    interface on a local machine can be found in the `www/README.md` file
