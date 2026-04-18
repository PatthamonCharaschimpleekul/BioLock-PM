import pandas as pd
import numpy as np
import joblib

# 1. LOAD MODEL & SCALERS
try:
    model = joblib.load('palf_model_v2.pkl')
    scaler_X = joblib.load('scaler_X_v2.pkl')
    scaler_y = joblib.load('scaler_y_v2.pkl')
except FileNotFoundError:
    print("Error: Model files not found. Please run predictive_engine_v2.py first.")
    exit()

def run_design_optimization(target_velocity):
    thicknesses = np.linspace(0.001, 0.05, 100) # 0.5cm to 5cm
    orientations = np.linspace(0.1, 0.9, 10)
    
    potential_designs = []
    
    for t in thicknesses:
        for ori in orientations:
            input_data = pd.DataFrame([[t, ori, target_velocity]], 
                                     columns=['Thickness_m', 'Fiber_Orientation', 'Air_Velocity'])
            input_scaled = scaler_X.transform(input_data)
            
            # Predict Pressure and Efficiency
            preds_scaled = model.predict(input_scaled)
            preds = scaler_y.inverse_transform(preds_scaled)
            
            p_drop = preds[0][0]
            efficiency = preds[0][1]
            
            # condition (Constraints): 50 Pa (safety of air condition)
            if p_drop < 50:
                score = efficiency * 100 
                potential_designs.append({
                    'Thickness_cm': t * 100,
                    'Fiber_Curvature': ori,
                    'Pressure_Drop_Pa': p_drop,
                    'Efficiency_%': efficiency * 100,
                    'Score': score
                })
    
    if not potential_designs:
        return None
        
    return pd.DataFrame(potential_designs).sort_values(by='Score', ascending=False)

# simulation real environment 
target_v = 2.5
results = run_design_optimization(target_v)

if results is not None:
    best = results.iloc[0]
    print(f"🚀 --- AI Recommended Design for SolidWorks ---")
    print(f"1. Thickness (ความหนา): {best['Thickness_cm']:.2f} cm")
    print(f"2. Fiber Curvature (ความโค้งใย): {best['Fiber_Curvature']:.2f} (Scale 0-1)")
    print(f"3. Predicted Pressure Drop: {best['Pressure_Drop_Pa']:.2f} Pa (Safe Limit < 50)")
    print(f"4. Capture Efficiency: {best['Efficiency_%']:.2f} %")
    
    # Save as table
    results.to_csv('optimized_design_specs.csv', index=False)
else:
    print("No safe design found for this velocity. Consider a thinner filter.")