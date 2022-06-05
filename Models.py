print("Importing libraries...")
# Imports:

## General imports
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

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
    
    
    
# Polynomial Regression
import pandas as pd
import matplotlib.pyplot as plt
import xgboost
from sklearn.feature_selection import mutual_info_regression

#read the data
data = pd.read_csv('../../data/final_baseline_data.csv')

their_prediction = data['price day ahead']

data = data.drop(['generation fossil coal-derived gas', 'generation fossil oil shale', 
    'generation fossil peat', 'generation geothermal', 'generation marine', 
    'generation wind offshore', 'forecast solar day ahead', 'forecast wind onshore day ahead',
    'total load forecast', 'price day ahead'], axis = 1)
    
#set x and y values
y = data['price actual']
x = data['total load actual']


import numpy as np
import matplotlib.pyplot as plt
import mpl_scatter_density
from matplotlib.colors import LinearSegmentedColormap
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import operator
from sklearn.model_selection import train_test_split

#set up for density plots
white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0, '#ffffff'),
    (1e-20, '#440053'),
    (0.2, '#404388'),
    (0.4, '#2a788e'),
    (0.6, '#21a784'),
    (0.8, '#78d151'),
    (1, '#fde624'),
], N=256)

#function for density plot
def scatter_density(fig, x, y):
    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=white_viridis)
    fig.colorbar(density, label='Density')

from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline

#polynomial regression using ridge regulation
def ridge(x, y, d):
    x_test, x_train, y_test, y_train = train_test_split(x, y, test_size = 0.2)
    p = PolynomialFeatures(degree = d)
    x_poly_test = p.fit_transform(x_test.values.reshape(-1, 1))
    x_poly_train = p.fit_transform(x_train.values.reshape(-1, 1))
    steps = [('poly', p), ('model', Ridge(alpha = 10, fit_intercept = True))]
    ridge_pipe = Pipeline(steps)
    ridge_pipe.fit(x_poly_train, y_train)
    y_train_pred = ridge_pipe.predict(x_poly_train)
    y_test_pred = ridge_pipe.predict(x_poly_test)

    print('Training Mean Squared Error ', mean_squared_error(y_train, y_train_pred))
    print('Testing Mean Squared Error ', mean_squared_error(y_test, y_test_pred))
    print('Training score: ', ridge_pipe.score(x_poly_train, y_train))
    print('Testing score: ', ridge_pipe.score(x_poly_test, y_test))

    fig = plt.figure()
    scatter_density(fig, x, y)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x_train, y_train_pred), key = sort_axis)
    x_poly_train, y_train_pred = zip(*sorted_zip)
    plt.plot(x_poly_train, y_train_pred, 'r')
    plt.show()

    return model, x_train, x_test, y_train, y_test


#get model
poly_reg = ridge(x, y, 3)
