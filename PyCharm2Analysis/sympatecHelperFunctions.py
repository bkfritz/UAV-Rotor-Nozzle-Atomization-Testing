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

def readSympatecData(filename):

    df = pd.read_csv(filename, encoding='latin1')

    Columns = ['Date','Time','Range','Optical Conc','Solution','Nozzle','Orientation',
                'Orifice','Pressure','Traverse','Airspeed','Traverse Speed','Meas Distance',
                'Rep','DV10','DV50','DV90','%<30um','%<50um','%<80um','%>100um',
                '%>141um','%>150um','%>200um','%>730um','Ch 1','Ch 2','Ch 3','Ch 4',
                'Ch 5','Ch 6','Ch 7','Ch 8','Ch 9','Ch 10','Ch 11','Ch 12',
                'Ch 13','Ch 14','Ch 15','Ch 16','Ch 17','Ch 18','Ch 19','Ch 20',
                'Ch 21','Ch 22','Ch 23','Ch 24','Ch 25','Ch 26','Ch 27','Ch 28',
                'Ch 29','Ch 30','Ch 31']
        
    df.columns = Columns

    df['Optical Conc'] = df['Optical Conc'].str.replace('%','').astype(float)

    return df

def sliceFullTraverse(df):
    '''
    Slice the full traverse data to a separate dataframe
    '''
    fullTraverse = df[df['Traverse'] == 'Full'].reset_index(drop=True)
    return fullTraverse

def getMeanData(df, columns):
    '''
    Get mean data for a given dataframe and columns
    '''
    meanDf = df.groupby(columns, as_index=False).mean()
    return meanDf

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
#
# def getNozzleData(meanData):
#     '''
#     Get the nozzle data for a given meanData dataframe
#     '''
#     nozzleData = ds.Nozzle()
#     # get nozzle name from meanData
#     name = str(meanData['Nozzle'][0])
#     # get fan angle from name string by removing the last 2 characters and converting to int
#     fan_angle = int(name[:-2])
#     # get orifice from meanData
#     orifice = meanData['Orifice'][0]
#     # get pressure from meanData
#     pressure = meanData['Pressure'][0]
#     # Set the data in nozzleData
#     nozzleData.setData(name, fan_angle, orifice, pressure, 0)
#     return nozzleData
#
# def getMeasurementConditions(df):
#
#     # get measurement conditions
#     measurement_conditions = ds.MeasurementConditions()
#     # get distane from nozzle
#     distance_from_nozzle = df['Meas Distance'][0]
#     # get airspeed
#     airspeed = df['Airspeed'][0]
#     # get traverse type
#     traverse_type = df['Traverse'][0]
#     # get traverse speed
#     traverse_speed = df['Traverse Speed'][0]
#
#     # set the measurement conditions
#     measurement_conditions.setData(distance_from_nozzle, airspeed, traverse_type, traverse_speed, 'Sympatec')
#
#     return measurement_conditions
#
# def getInstrumentData(instrument_type, df):
#     '''
#     This function sets the instrument data for the instrument object
#     '''
#     instrument = ds.Instrument()
#     # If sympatec data, name = Sympatec, if oxford laser data, name = Oxford Laser
#     # If name = Sympatec, get lens as first two letters of the Range data
#     if instrument_type == 'Sympatec':
#         lens_mag = df['Range'].str[0:2].unique()[0]
#
#     # Set instrument data
#     instrument.setData(instrument_type, lens_mag)
#     return instrument
#
#
# def getSolutionData(df):
#     # Solution data
#     solution_data = ds.Solution()
#     # Set solution name as the Solution column in the meanData dataframe
#     solution = df['Solution'].unique()[0]
#     solution_data.setData(solution, 1.0, 1.0, 1.0)
#
#     return solution_data
#
#
# def getVolumeDiamData(df):
#     # Get volume diameter data, dv10
#     dv10 = df['DV10'][0]
#     dv50 = df['DV50'][0]
#     dv90 = df['DV90'][0]
#     optical_conc = df['Optical Conc'][0]
#
#     vol_diams = ds.VolumeDiameters()
#     vol_diams.setData(dv10, dv50, dv90, optical_conc)
#
#     return vol_diams
#
#
# def getDistributionData(df, dia_bins):
#     # Set distribution data
#     dist_data = ds.DistributionData()
#
#     # Distribution results for the Sympatec data are the last 31 columns
#     distribution = df.iloc[:, -31:].values.tolist()[0]
#
#     dist_data.setData(distribution, dia_bins)
#
#     return dist_data



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

