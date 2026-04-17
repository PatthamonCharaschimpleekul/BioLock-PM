import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputRegressor

#load generated data
try:
    df = pd.read_csv('palf_training_data_v2.csv')
except FileNotFoundError:
    print("Please run aerodynamic_model.py first to generate the dataset!")
    exit()

#preprocessing
X = df[['Thickness_m', 'Fiber_Orientation', 'Air_Velocity']]
y = df[['Pressure_Drop_Pa', 'Capture_Efficiency']]

#SVR is sensitive to feature scales, so we MUST use StandardScaler
scaler_X = StandardScaler()
scaler_y = StandardScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

#SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

#TRAIN SVR MODEL (multioutput)
base_svr = SVR(kernel='rbf', C=100, epsilon=0.01)
model = MultiOutputRegressor(base_svr)
model.fit(X_train, y_train)

joblib.dump(model, 'palf_model_v2.pkl')
joblib.dump(scaler_X, 'scaler_X_v2.pkl')
joblib.dump(scaler_y, 'scaler_y_v2.pkl')

print("Multi-output SVR Training Complete. Model saved as palf_model_v2.pkl")