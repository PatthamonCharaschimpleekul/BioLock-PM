import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

#load generated data
try:
    df = pd.read_csv('aerodinamic_model.py')
except FileNotFoundError:
    print("Please run aerodynamic_model.py first to generate the dataset!")
    exit()

#preprocessing
#Features: Velocity, Permeability, Thickness
X = df[['Velocity_ms', 'Permeability_k', 'Thickness_m']]
y = df['PressureDrop_Pa']

#SVR is sensitive to feature scales, so we MUST use StandardScaler
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1,1)).ravel()