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
a flux value calculdated from the Oxford Laser data.

This file is the first step in the process.  It reads in the Sympatec data and does
some initial processing to get the data into a format that can be further used.

'''

import pandas as pd
import numpy as np
from csv import reader
import dataStuctures as ds


def sliceDataframeByColumns(df, columns):
    '''
    Slice a dataframe by a list of columns
    '''
    slicedDf = df[columns].reset_index(drop=True)
    return slicedDf


def weighted_average(df, data_col, weight_col):
    """ Calculate weighted average of a DataFrame column. """
    return np.average(df[data_col], weights=df[weight_col])

# For index of the nozzlePressureAirspeedTraverseSpeed dataframe and
# slice out the data for each set
def getSpecificTreatmentData(df, nozzlePressureAirspeedTraverseSpeed, index):
    '''
    Get the data for a specific nozzle, pressure, airspeed, and traverse speed
    '''
    data = df[(df['Nozzle'] == nozzlePressureAirspeedTraverseSpeed['Nozzle'][index]) &
                        (df['Pressure'] == nozzlePressureAirspeedTraverseSpeed['Pressure'][index]) &
                        (df['Airspeed'] == nozzlePressureAirspeedTraverseSpeed['Airspeed'][index]) &
                        (df['Traverse Speed'] == nozzlePressureAirspeedTraverseSpeed['Traverse Speed'][index])].reset_index(drop=True)
    return data

def getNozzleData(meanData):
    '''
    Get the nozzle data for a given meanData dataframe
    '''
    nozzleData = ds.Nozzle()
    # get nozzle name from meanData
    name = str(meanData['Nozzle'][0])
    # get fan angle from name string by removing the last 2 characters and converting to int
    fan_angle = int(name[:-2])
    # get orifice from meanData
    orifice = meanData['Orifice'][0]
    # get pressure from meanData
    pressure = meanData['Pressure'][0]
    # Set the data in nozzleData
    nozzleData.setData(name, fan_angle, orifice, pressure, 0)
    return nozzleData

def getMeasurementConditions(df):

    # get measurement conditions
    measurement_conditions = ds.MeasurementConditions()
    # get distane from nozzle
    distance_from_nozzle = df['Meas Distance'][0]
    # get airspeed
    airspeed = df['Airspeed'][0]
    # get traverse type
    traverse_type = df['Traverse'][0]
    # get traverse speed
    traverse_speed = df['Traverse Speed'][0]

    # set the measurement conditions
    measurement_conditions.setData(distance_from_nozzle, airspeed, traverse_type, traverse_speed, 'Sympatec')

    return measurement_conditions

# Function to get the weighted average of DV10, DV50, DV90 for a given nozzle.

# def getWeightedAvg(nozzle, df):

#     # Mean dataframe grouped by Nozzle, Orientation, Orifice, Pressure, Traverse, Airspeed, Traverse Speed as_index=False
#     meanDf = df.groupby(['Nozzle','Orientation','Orifice','Pressure','Traverse','Airspeed','Traverse Speed'], as_index=False).mean()

#     # Slice out data for each nozzle
#     nozzle_df = meanDf[meanDf['Nozzle'] == nozzle].reset_index(drop=True)

#     # Slice out Full traverse data for each nozzle
#     nozzleFull = nozzle_df[nozzle_df['Traverse'] == 'Full'].reset_index(drop=True)

#     # Slice out non-Full traverse data for each nozzle
#     nozzleNonFull = nozzle_df[nozzle_df['Traverse'] != 'Full'].reset_index(drop=True)

#     '''
#     For the nozzleNonFull data, calculate the mean DV10, DV50, and DV90 using all traverse
#     positions by weighting each value at each position by the optical concentration at that
#     position.
#     '''

#     # calculate the weighted averages for each nozzle type
#     grouped = nozzleNonFull.groupby('Nozzle')
#     results = pd.DataFrame({
#         'DV10': grouped.apply(weighted_average, 'DV10', 'Optical Conc'),
#         'DV50': grouped.apply(weighted_average, 'DV50', 'Optical Conc'),
#         'DV90': grouped.apply(weighted_average, 'DV90', 'Optical Conc')
#     })

#     # merge the mean data with the weighted averages
#     merged_df = pd.merge(results.reset_index(), nozzleFull, on='Nozzle', suffixes=('_weighted', '_mean'))

#     return nozzleFull, nozzleNonFull, merged_df

# 11001 nozzle data
# nozzle1 = 11001
# vf_f_full, vf_f_locations, merged_vf_f = getWeightedAvg(nozzle1, newDf)

