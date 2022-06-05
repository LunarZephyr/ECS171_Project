# ECS171 Group 25 Final Project

The Github repo has the following structure:

- The `data` folder contains the raw csv files from our
  [dataset](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather) in addition to the final version of processed data.
- The `EDA` folder contains exploratory data analysis performed by each team member
  on the csv files.
- `Models.py` contains the raw code from the notebooks to run all three models discussed in the report in a terminal environment.
  - All models from this file are saved to the `savedmodels` directory.
  - All figires from this file are saved to the `figures` directory.
- The notebooks with individual models are located in the `FinalModelNotebooks` directory.
  - The `Models_XGBoost_and_SHAP.ipynb` file contains the source code for our XGBoost model for price prediction and the SHAP analysis.
    - Please note: that GridSearch for the XGBoost Price Model is in `EDA/Claire/xgboost.ipynb`.  Unfortunately, it took too long to recreate (to run and show the output, it took about 5 hours) in `Models_XGBoost_and_SHAP.ipynb`.  Apologies for this!
  - The `Models_Neural_Net.ipynb` contains the neural network with tuned hyperparameters.
  - The `Models_polynomial_regression.ipynb` contains the polynomial regression notebook.
  - The data-wrangling and data-engineering notebook `Dataset_Engineering_Preparation.ipynb` contains feature engineering and preparing a baseline training and testing for our XGBoost price model (the data used in the NN model and how it was constructed from the raw csvs can be seen in `Models_Neural_Network.ipynb` and `EDA/Ameya/removeDuplicates.py`)
  - The resulting data file from running this notebook that is used to train the models is called `final_baseline_data.csv`
- The `Report` folder contains the tex file of our final report along with the
  images used.
- The `www` folder contains the source code of
  our project website.
  - Instructions on running the flask back-end and interacting with the web
    interface on a local machine can be found in the `www/README.md` file
