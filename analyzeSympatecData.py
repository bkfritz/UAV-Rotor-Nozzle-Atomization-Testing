'''
This script is written to read in and and process Sympatec data from a study 
comparing it to the Oxford Laser P15 data from the same study. The data is
reference nozzle data evaluated in the low speed wind tunnel.  The following measurements and
measurment conditions.
Sympatec:
All reference nozzles
- Full traverse at 1 and 2 in/s
- Every inch along the spray plume (Traverse Speed shown as 1 in/s should be 0)

Oxford Laser:
All reference nozzles
- Full traverse at 2 in/s
- Every inch along the spray plume (Traverse Speed shown as 1 in/s should be 0)

Patternator Data as done by UNL PAT Lab group.
Each reference nozzle was evaluated for spray deposit rate every inch along the spray plume
at a height of 12 in.  This data will be compared to the Sympatec optical concentration and
a flux value calculated from the Oxford Laser data.

This file is the step by step process of analyzing that data using functions from the
sympatecHelperFunctions.py file.

'''

import pandas as pd
import numpy as np
from sympatecHelperFunctions import readSympatecData, sliceFullTraverse, getMeanData
from sympatecHelperFunctions import sliceDataframeByColumns, getSpecificTreatmentData
from sympatecHelperFunctions import getNozzleData, getMeasurementConditions
from matplotlib import pyplot as plt
import dataStuctures as ds

sympatec = readSympatecData(filename = 'All Sympatec Data.txt')

# Slice out only the columens we need
columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse', 
           'Traverse Speed', 'Meas Distance', 'DV10', 'DV50', 'DV90',
           'Optical Conc', 'Ch 1', 'Ch 2', 'Ch 3', 'Ch 4', 'Ch 5', 'Ch 6',
           'Ch 7', 'Ch 8', 'Ch 9', 'Ch 10', 'Ch 11', 'Ch 12', 'Ch 13', 'Ch 14',
           'Ch 15', 'Ch 16', 'Ch 17', 'Ch 18', 'Ch 19', 'Ch 20', 'Ch 21', 'Ch 22',
           'Ch 23', 'Ch 24', 'Ch 25', 'Ch 26', 'Ch 27', 'Ch 28', 'Ch 29', 'Ch 30',
           'Ch 31']
sympatec = sliceDataframeByColumns(sympatec, columns)

# Start by looking at the full traverse data
fullTraverse = sliceFullTraverse(sympatec)

# Get list of unique nozzles
nozzles = fullTraverse['Nozzle'].unique()

# Get list of unique combination sets of nozzle, pressure, airspeed, and traverse speed
# This will be used to slice out the data for each set
nozzlePressureAirspeedTraverseSpeed = fullTraverse[['Nozzle', 
                    'Pressure', 'Airspeed', 'Traverse Speed']].drop_duplicates().reset_index(drop=True)

# Get a list of the indexes for in nozzlePressureAirspeedTraverseSpeed
indicies = nozzlePressureAirspeedTraverseSpeed.index.tolist()

i = 0
ind = indicies[i]

# Get the data for the first nozzle, pressure, airspeed, and traverse speed
data = getSpecificTreatmentData(fullTraverse, nozzlePressureAirspeedTraverseSpeed, ind)     

mean_columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse', 
           'Traverse Speed', 'Meas Distance']

# mean_columns are those by which to group the data to get the mean
mean_columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse',
                'Traverse Speed', 'Meas Distance']

meanData = getMeanData(data, mean_columns)

noz_data = getNozzleData(meanData)

meas_conds = getMeasurementConditions(meanData)

# get instrument data
instrument = ds.Instrument()








