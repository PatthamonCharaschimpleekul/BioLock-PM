import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

#load generated data
try:
    df = pd.read_csv('biofilter_simulation_data.csv')
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

#SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

#TRAIN SVR MODEL
#Regularization, epsilon: Margin of tolerance
model = SVR(kernel='rbf', C=100, epsilon=0.1)
model.fit(X_train, y_train)

#EVALUATION
y_pred_scaled = model.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
y_test_unscaled = scaler_y.inverse_transform(y_test.reshape(-1, 1))

r2 = r2_score(y_test_unscaled, y_pred)
mae = mean_absolute_error(y_test_unscaled, y_pred)

print(f"--- SVR Model Performance ---")
print(f"R2 Score: {r2:.4f}")
print(f"Mean Absolute Error: {mae:.2f} Pa")

#"DIGITAL TWIN" PREDICTION FUNCTION
def predict_filter_safety(v, k, t):
    input_df = pd.DataFrame([[v, k, t]], columns=['Velocity_ms', 'Permeability_k', 'Thickness_m'])
    input_data = scaler_X.transform(input_df)
    prediction_scaled = model.predict(input_data)
    prediction = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1))
    return prediction[0][0]

# Example: Predicting for a new custom 3cm filter
test_val = predict_filter_safety(2.8, 2.5e-9, 0.03)
print(f"\nPredicted Pressure Drop for 3cm filter at 2.8m/s: {test_val:.2f} Pa")