print("Importing libraries...")
# Imports:

## General imports
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

## Data preprocessing imports
from sklearn.model_selection import train_test_split

## Model Evaluation imports
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

## Neural network imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import metrics as tfmetrics

print("Beginning the Neural Network training:")
print("Starting data preprocessing...")
# import valid csv files
Energy = pd.read_csv('./data/energy_dataset.csv')
Energy = Energy[Energy['total load actual'].notna()]
Weather = pd.read_csv('./EDA/Ameya/AllTemps.csv', skipinitialspace=True)

# Get weighted averages of the weather data, as well as integer representation of time
pops2017 = {"V": 788000, "M": 3183000, "Bi": 345000, "Ba": 1621000, "S": 689000}
totalPop2017= 788000 + 3183000 + 345000 + 1621000 + 689000
pops2017["V"] /= totalPop2017
pops2017["M"] /= totalPop2017
pops2017["Bi"] /= totalPop2017
pops2017["Ba"] /= totalPop2017
pops2017["S"] /= totalPop2017
def WeightedAverages(Wvar, row, pops):
    return (pops["V"] * row[Wvar + "V"]) + (pops["M"] * row[Wvar + "M"]) + (pops["Bi"] * row[Wvar + "Bi"]) + (pops["Ba"] * row[Wvar + "Ba"]) + (pops["S"] * row[Wvar + "S"])
def IsolateHour(Time):
    Time = Time.split(" ")
    Time = Time[1].split(":")
    return Time[0]
IntTimes = []
TempsAverage = []
HumAvererage = []
CldAverage = []
WndAverage = []
for index, row in Weather.iterrows():
    TempsAverage.append(WeightedAverages("temp", row, pops2017))
    HumAvererage.append(WeightedAverages("hum", row, pops2017))
    CldAverage.append(WeightedAverages("cld", row, pops2017))
    WndAverage.append(WeightedAverages("wnd", row, pops2017))
    IntTimes.append(IsolateHour(row["time"]))
WxAverages = pd.DataFrame({
    "time": np.asarray(IntTimes).astype('float64'),
    "tAve": np.asarray(TempsAverage).astype('float64'),
    "hAve": np.asarray(HumAvererage).astype('float64'),
    "cAve": np.asarray(CldAverage).astype('float64'),
    "wAve": np.asarray(WndAverage).astype('float64')
})

# Scale the data with the MinMax method
colScales = []
colMins = []
def MinMaxScaler(column):
    scale = max(column)-min(column)
    colScales.append(scale)
    colMins.append(min(column))
    return (column-min(column))/scale   
for col in WxAverages.columns:
    WxAverages[col] =   MinMaxScaler(WxAverages[col])
load = MinMaxScaler(Energy['total load actual'])


print("Creating and training the model. This may take a while...")
# Function to create model
def create_model(h1=3, h2=3):
    model = Sequential()
    layers = [
        Dense(5, activation='elu', name='input', kernel_initializer="normal"),
        Dense(h1, activation='elu', name='h1', kernel_initializer="normal"),
        Dense(h2, activation='elu', name='h2', kernel_initializer="normal"),
        Dense(1, activation='tanh', name='out', kernel_initializer="normal")
    ]
    for layer in layers:
        model.add(layer)
    model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001), metrics=[tfmetrics.RootMeanSquaredError()])
    return model

# Create the model
loadNN = create_model()

# Create testing and training dataset
wxtrain, wxtest, loadtrain, loadtest = train_test_split(WxAverages, load, test_size = 0.1, random_state=0)

# Train the model
hist = loadNN.fit(wxtrain.to_numpy(), loadtrain.to_numpy(), epochs=500, verbose=0)
print("Finished training model.")


# Get evaluation scores
load_pred = loadNN.predict(wxtest, verbose=0)
MSE = mean_squared_error(y_true=loadtest, y_pred=load_pred)
RMSE = mean_squared_error(y_true=loadtest, y_pred=load_pred, squared=False)
r2 = r2_score(y_true=loadtest, y_pred=load_pred)
print("Load Neural Network Scores:")
print('Testing MSE: %.5f' % MSE)
print('Testing RMSE: %.5f' % RMSE)
print("r^2 score: %.5f" % r2)

# Save the model to disk
uInput = ""
while ((uInput != "y") and (uInput != "n")):
    uInput = input("Would you like to save the neural network to disk (y/n)?")
if uInput == "y":
    loadNN.save('./savedmodels/LoadNN.ann')
    print("NN saved to /savedmodels/LoadNN.ann")
