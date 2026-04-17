import numpy as np
import pandas as pd

class PALF_BioFilter_Model:
    def __init__(self):
        self.air_viscosity = 1.81e-5
        self.dielectric_constant = 2.5 # Approximate for PALF
        self.pm25_diameter = 2.5e-6   # 2.5 micrometers
        
    def calculate_efficiency(self, thickness, velocity, porosity, electrostatic_charge):
        """
        Calculates Total Efficiency = Mechanical Capture + Electrostatic Capture
        """
        # Mechanical capture (Impaction & Interception)
        η_mech = 1 - np.exp(-(1 - porosity) * thickness / (porosity * 1e-4))
        
        # Electrostatic capture (Simplified Coulombic model)
        η_elec = (electrostatic_charge * 1e-6) / (velocity + 1e-9) 
        
        total_η = min(η_mech + η_elec, 0.99) # Max 99%
        return total_η

    def generate_fiber_dataset(self):
        # Range 0-5 cm (0.00 to 0.05 m)
        thicknesses = np.linspace(0.0, 0.05, 50) 
        # Simulation of Fiber Orientation: 0 (Straight) to 1 (Highly Curved/Entangled)
        orientations = np.linspace(0, 1, 5) 
        
        results = []
        for t in thicknesses:
            for ori in orientations:
                v = 2.5 # Fixed at typical AC speed
                # Fiber curvature increases air resistance (Tortuosity)
                k = 5e-9 * (1 - (ori * 0.5)) 
                
                # Pressure Drop Calculation
                dp = (self.air_viscosity * t * v) / (k + 1e-12)
                
                # PM2.5 Capture Efficiency
                eff = self.calculate_efficiency(t, v, 0.85, ori * 10)
                
                results.append({
                    'Thickness_m': t,
                    'Fiber_Curvature': ori,
                    'PressureDrop_Pa': dp,
                    'Capture_Efficiency': eff
                })
        return pd.DataFrame(results)

model = PALF_BioFilter_Model()
df_v2 = model.generate_fiber_dataset()
df_v2.to_csv('palf_advanced_data.csv', index=False)