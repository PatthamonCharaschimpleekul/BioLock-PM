import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BioFilterSim:
    def __init__(self):
        # Empirical constants for Pineapple Leaf Fiber (PALF)
        # Based on typical natural fiber composite research
        self.air_viscosity = 1.81e-5  # Pa·s (at 15-40°C)
        self.air_idensity = 1.225 #kg/m^3
    
    def calculate_pressure_drop(self, velocity, thickness, permeability):
        """
        Calculates Pressure Drop (delta P) using Darcy's Law.
        Formula: delta_P = (viscosity * thickness * velocity) / permeability
        """
        delta_p = (self.air_viscosity * thickness * velocity) / permeability
        return delta_p
    
    def run_optimization_study(self):
        #Create dataset (1cm to 5cm)
        #Permeability (k) based on fiber packing density
        thicknesses = np.linspace(0.01,0.01,10)
        velocities = [2.0,2.5,3.0]

        #high permeability (loose fiber) vs low permeability (dense fiber)
        permeability_range = [1.0e-9, 5.0e-9, 1.0e-8]

        results = []
        for v in velocities:
            for k in permeability_range:
                for t in thicknesses:
                    dp = self.calculate_pressure_drop(v, t, k)
                    results.append({
                        'Velocity_ms':v,
                        'Permeability_k':k,
                        'Thickness_m':t,
                        'PressureDrop_pa':dp,
                        'Safe_Limit': dp < 50 # 50 Pa is a common safety threshold
                    })
        return pd.DataFrame(results)

#execution
sim = BioFilterSim()
df = sim.run_optimization_study()

# Filter for the most efficient "Safe" configuration
optimal_configs = df[df['Safe_Limit'] == True].sort_values(by='PressureDrop_Pa')

print("--- Top 5 Optimal Filter Configurations (Safe Range) ---")
print(optimal_configs.head())

# Save dataset for GitHub Portfolio
df.to_csv('biofilter_simulation_data.csv', index=False)