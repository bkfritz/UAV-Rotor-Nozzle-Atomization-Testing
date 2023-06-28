# Defining a class for the Sympatec data and functions to analyze it.

import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class SympatecData:
    # This class will be used to read in the Sympatec data as well as hold processed data.
    # The class will have methods to process the data and return the processed data.
    raw_data: pd.DataFrame = None
    dv10: float = None
    dv50: float = None
    dv90: float = None
    optical_conc: float = None
    pressure: float = None
    traverse_speed: float = None
    airspeed: float = None
    nozzle: int = None
    orientation: str = None
    orifice: float = None
    solution: str = None
    diameter_bins: list = None

    def getRawData(self, raw_data):
        self.raw_data = raw_data

    def getDiameterVolumeData(self, dv10, dv50, dv90):
        self.dv10 = dv10
        self.dv50 = dv50
        self.dv90 = dv90
    
    def getOpticalConcentration(self, optical_conc):
        self.optical_conc = optical_conc

    def getSettingsData(self, pressure, traverse_speed, airspeed, nozzle, orientation, orifice, solution):
        self.pressure = pressure
        self.traverse_speed = traverse_speed
        self.airspeed = airspeed
        self.nozzle = nozzle
        self.orientation = orientation
        self.orifice = orifice
        self.solution = solution