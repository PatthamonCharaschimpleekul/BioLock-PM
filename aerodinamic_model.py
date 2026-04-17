import numpy as np
import pandas as pd

class PALF_BioFilter_Model:
    def __init__(self):
        self.air_viscosity = 1.81e-5
        self.pm25_diameter = 2.5e-6   # 2.5 micrometers
        
    def calculate_physics(self, thickness, velocity, orientation):
        """
        calculate pressure drop and efficiency reference from Micro-structure
        """
        # Permeability decrease when fiber is complex and curve (high orientation)
        k_base = 5e-9 
        k_effective = k_base * (1 - (orientation * 0.6))
        
        # Pressure Drop (Darcy's Law)
        p_drop = (self.air_viscosity * thickness * velocity) / (k_effective + 1e-12)
        
        # 2. Efficiency (Mechanical + Electrostatic)
        # High tortuosity high efficiency
        mechanical_eff = 1 - np.exp(-(1.5 * orientation * thickness) / (1e-4))
        
        electrostatic_eff = (orientation * 0.2) / (velocity + 0.1)
        total_efficiency = min(mechanical_eff + electrostatic_eff, 0.98) # Max 98%
        return p_drop, total_efficiency

    def generate_dataset(self):
        # thickness 0-5 cm (0.00 - 0.05 m)
        thicknesses = np.linspace(0.001, 0.05, 100) 
        # curve 0 (straight) to 1 
        orientations = np.linspace(0.1, 0.9, 10)
        velocities = [2.0, 2.5, 3.0, 3.5] # ความเร็วลมพัดลมแอร์
        
        data = []
        for t in thicknesses:
            for ori in orientations:
                for v in velocities:
                    dp, eff = self.calculate_physics(t, v, ori)
                    data.append({
                        'Thickness_m': t,
                        'Fiber_Orientation': ori,
                        'Air_Velocity': v,
                        'Pressure_Drop_Pa': dp,
                        'Capture_Efficiency': eff
                    })
        return pd.DataFrame(data)

# create and save
model = PALF_BioFilter_Model()
new_df = model.generate_dataset()
new_df.to_csv('palf_training_data_v2.csv', index=False)
print("New training data generated: palf_training_data_v2.csv")