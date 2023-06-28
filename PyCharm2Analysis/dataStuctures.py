# Defining a class for the Sympatec data and functions to analyze it.

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List

@dataclass
class VolumeDiameters:
    dv10: float = 0.0
    dv50: float = 0.0
    dv90: float = 0.0
    optical_conc: float = 0.0

    def setData(self, dv10, dv50, dv90, optical_conc):
        self.dv10 = dv10
        self.dv50 = dv50
        self.dv90 = dv90
        self.optical_conc = optical_conc

@dataclass
class DistributionData:
    diameter_bins: list = field(default_factory=list)
    distribution: list = field(default_factory=list)

    def setData(self, diameter_bins, distribution):
        self.diameter_bins = diameter_bins
        self.distribution = distribution

@dataclass
class Nozzle:
    name: str = ''
    fan_angle: int = 0
    orifice: float = 0
    pressure: float = 0
    flowrate: float = 0

    def setData(self, name, fan_angle, orifice, pressure, flowrate):
        self.name = name
        self.fan_angle = fan_angle
        self.orifice = orifice
        self.pressure = pressure
        self.flowrate = flowrate

@dataclass
class MeasurementConditions:
    distance_from_nozzle: float = 0.0 # Distance from nozzle in in
    airspeed: float = 0.0 # Airspeed in mph
    traverse_location: str = 'Full' # 'Full or a number for Spot'
    traverse_speed: float = 0.0 # Traverse speed in in/s

    def setData(self, distance_from_nozzle, airspeed, traverse_type, traverse_speed, instrument):
        self.distance_from_nozzle = distance_from_nozzle
        self.airspeed = airspeed
        if traverse_type == 'Full':
            self.traverse_location = traverse_type
        else:
            self.traverse_location = float(traverse_type)
        self.traverse_speed = traverse_speed
        self.instrument = instrument

@dataclass
class Instrument:
    name: str = 'Sympatec'

    lens_mag: float = 'R7' # Either R6 or R7 for Symptec, or magnification for Malvern
    # set the diameter bins default using default_factory
    diam_bins: list = field(default_factory=list)

    def setData(self, name, lens_mag):
        self.name = name
        if self.name == 'Sympatec':
            self.lens_mag = lens_mag
            if lens_mag == 'R6':
                self.diam_bins = [9, 11, 13, 15, 18, 22, 26, 31, 37, 43, 50, 60, 75, 90, 105, 120, 150, 180, 210, 250, 300,
                    360, 430, 510, 610, 730, 870, 1030, 1230, 1470, 1750]
            elif lens_mag == 'R7':
                self.diam_bins = [18, 22, 26, 30, 36, 44, 52, 62, 74, 86, 100, 120, 150, 180, 210, 250, 300, 360, 420, 500,
                    600, 720, 860, 1020, 1220, 1460, 1740, 2060, 2460, 2940, 3500]

@dataclass
class Solution:
    name: str = 'Water'
    density: float = 1.0 # Density in g/cm^3
    viscosity: float = 1.0 # Viscosity in cP
    surface_tension: float = 1.0 # Surface tension in dynes/cm

    def setData(self, name, density, viscosity, surface_tension):
        self.name = name
        self.density = density
        self.viscosity = viscosity
        self.surface_tension = surface_tension

@dataclass
class MeasuredData:
    name: str
    nozzle: Nozzle
    solution: Solution
    instrument: Instrument
    measurement_conditions: MeasurementConditions
    volume_diameters: VolumeDiameters
    distribution: DistributionData

@dataclass
class AllResultData:
    measuredData: list = field(default_factory=list)

    def addMeasuredData(self, measuredData):
        self.measuredData.append(measuredData)


