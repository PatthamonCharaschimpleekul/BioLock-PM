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
    