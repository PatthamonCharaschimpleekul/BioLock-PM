import pandas as pd
import numpy as np
import joblib

# LOAD MODEL & SCALERS
try:
    model = joblib.load('palf_model_v2.pkl')
    scaler_X = joblib.load('scaler_X_v2.pkl')
    scaler_y = joblib.load('scaler_y_v2.pkl')
except FileNotFoundError:
    print("Error: Required model files missing. Run predictive_engine_v2.py first.")
    exit()

def run_exhaustive_simulation(target_velocity):
    # Defining the range: 0.1cm to 5.0cm (1mm steps)
    # Removing rounding to keep raw floating point precision
    thickness_range = np.linspace(0.001, 0.05, 50) 
    # Testing multiple curvatures to find the interaction effects
    curvature_range = np.linspace(0.1, 0.9, 9)
    
    all_results = []
    
    #print(f"{'Thickness (m)':<18} | {'Curvature':<10} | {'Pressure (Pa)':<15} | {'Efficiency (%)':<15} | {'Status'}")
    #print("-" * 85)
    
    for t in thickness_range:
        for c in curvature_range:
            # Prepare raw input for AI
            input_df = pd.DataFrame([[t, c, target_velocity]], 
                                     columns=['Thickness_m', 'Fiber_Orientation', 'Air_Velocity'])
            
            # AI Inference
            input_scaled = scaler_X.transform(input_df)
            preds_scaled = model.predict(input_scaled)
            preds = scaler_y.inverse_transform(preds_scaled)
            
            p_drop = preds[0][0]
            eff = preds[0][1] * 100
            
            status = "PASS" if p_drop < 50 else "FAIL"
            
            # Log raw data to console
            #print(f"{t:<18.6f} | {c:<10.2f} | {p_drop:<15.4f} | {eff:<15.4f} | {status}")
            
            # Store all data points for CSV export
            all_results.append({
                'Thickness_m': t,
                'Fiber_Curvature': c,
                'Air_Velocity_ms': target_velocity,
                'Pressure_Drop_Pa': p_drop,
                'Efficiency_Percentage': eff,
                'Safety_Status': status
            })

    # Save to CSV
    df_output = pd.DataFrame(all_results)
    df_output.to_csv('full_design_matrix.csv', index=False)
    print(f"Simulation Complete. {len(df_output)} data points saved to 'full_design_matrix.csv'")
    return df_output

# EXECUTION
# Simulating for standard AC outdoor unit fan speed
final_results = run_exhaustive_simulation(target_velocity=2.5)