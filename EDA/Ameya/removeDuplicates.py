import pandas as pd
import numpy as np

Weather = pd.read_csv('../../data/weather_features.csv', skipinitialspace=True)
EnergySub = pd.read_csv('../../data/energy_dataset.csv')

WV = {
    'tempV': np.array(Weather.loc[Weather['city_name'] == 'Valencia', 'temp']),
    'timeWV': np.array(Weather.loc[Weather['city_name'] == 'Valencia', 'dt_iso']),
}
WM = {
    'tempM': np.array(Weather.loc[Weather['city_name'] == 'Madrid', 'temp']),
    'timeWM': np.array(Weather.loc[Weather['city_name'] == 'Madrid', 'dt_iso']),
}
WBi = {
    'tempBi': np.array(Weather.loc[Weather['city_name'] == 'Bilbao', 'temp']),
    'timeWBi': np.array(Weather.loc[Weather['city_name'] == 'Bilbao', 'dt_iso']),
}
WBa = {
    'tempBa': np.array(Weather.loc[Weather['city_name'] == 'Barcelona', 'temp']),
    'timeWBa': np.array(Weather.loc[Weather['city_name'] == 'Barcelona', 'dt_iso']),
}
WS = {
    'tempS': np.array(Weather.loc[Weather['city_name'] == 'Seville', 'temp']),
    'timeWS': np.array(Weather.loc[Weather['city_name'] == 'Seville', 'dt_iso']),
}
WV = pd.DataFrame(WV)
WM = pd.DataFrame(WM)
WBi = pd.DataFrame(WBi)
WBa = pd.DataFrame(WBa)
WS = pd.DataFrame(WS)

for i in range(len(EnergySub)):
    if (WV.iloc[i]['timeWV'] != EnergySub.iloc[i]['time']):
        WV.drop(i, inplace=True, axis=0)
        i -= 1
for i in range(len(EnergySub)):
    if (WM.iloc[i]['timeWM'] != EnergySub.iloc[i]['time']):
        WM.drop(i, inplace=True, axis=0)
        i -= 1
for i in range(len(EnergySub)):
    if (WBi.iloc[i]['timeWBi'] != EnergySub.iloc[i]['time']):
        WBi.drop(i, inplace=True, axis=0)
        i -= 1
for i in range(len(EnergySub)):
    if (WBa.iloc[i]['timeWBa'] != EnergySub.iloc[i]['time']):
        WBa.drop(i, inplace=True, axis=0)
        i -= 1
for i in range(len(EnergySub)):
    if (WS.iloc[i]['timeWS'] != EnergySub.iloc[i]['time']):
        WS.drop(i, inplace=True, axis=0)
        i -= 1

WeatherSub = pd.DataFrame ({
    'time': list(WV['timeWV']),
    'tempV': list(WV['tempV']),
    'tempM': list(WM['tempM']),
    'tempBi': list(WBi['tempBi']),
    'tempBa': list(WBa['tempBa']),
    'tempS': list(WS['tempS']),
})

WeatherSub.to_csv('AllTemps.csv')