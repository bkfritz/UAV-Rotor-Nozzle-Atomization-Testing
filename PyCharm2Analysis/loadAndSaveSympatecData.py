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

This file is the step by step process of analyzing that data using functions from the
sympatecHelperFunctions.py file.

Notes on what data comparisons to be made.
1. Compare Sympatec Full scan results at the different air and traverse speeds.
2. Examine the correlation between the Sympatec optical concentration and the patternator data
   at the different measurement locations for the spot measurements.
3. Determine the volume diameter data using the point data weighted by the optical concentration
    and compare to the full scan results.
4. Determine the diameter x velocity curves using the Oxford Data, and use to weight the
    Sympatec lower airspeed data to see if it brings into agreement with the higher airspeed data.
5. Compare Sympatec and Oxford full scan results at same airspeeds.
6. Using raw Oxford data, determine the flux at each measurement location and compare to the
    Sympatec optical concentration and the patternator data.
7. Using raw Oxford data, determine the volume (flux) weighted and velocity and volume weighted
    diameter data.
8. Main object is to determine the best approach to collected data for the UAV rotor wash
    measurements in which different setups will require multiple location measurements and
    will be further complicated by different airspeed conditions due to changes in rotor speed.


'''

import pandas as pd
import numpy as np
from sympatecHelperFunctions import readSympatecData, sliceFullTraverse, getMeanData
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import pickle

# Incrementer list creation function
def create_incrementer_list(length, bar_width):
    incrementer = []

    if length % 2 == 0:  # Even length
        half_length = length // 2
        incrementer = [(i - half_length + 0.5) * bar_width for i in range(length)]
    else:  # Odd length
        half_length = length // 2
        incrementer = [(i - half_length) * bar_width for i in range(length)]

    return incrementer


sympatec = readSympatecData(filename = 'All Sympatec Data.txt')

# Slice out only the columns we need
columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed',
           'Traverse', 'Traverse Speed', 'Meas Distance', 'DV10', 'DV50', 'DV90',
           'Optical Conc', 'Ch 1', 'Ch 2', 'Ch 3', 'Ch 4', 'Ch 5', 'Ch 6',
           'Ch 7', 'Ch 8', 'Ch 9', 'Ch 10', 'Ch 11', 'Ch 12', 'Ch 13', 'Ch 14',
           'Ch 15', 'Ch 16', 'Ch 17', 'Ch 18', 'Ch 19', 'Ch 20', 'Ch 21', 'Ch 22',
           'Ch 23', 'Ch 24', 'Ch 25', 'Ch 26', 'Ch 27', 'Ch 28', 'Ch 29', 'Ch 30',
           'Ch 31']

r6_bin = [9, 11, 13, 15, 18, 22, 26, 31, 37, 43, 50, 60, 75, 90, 105, 120, 150, 180, 210, 250, 300,
                      360, 430, 510, 610, 730, 870, 1030, 1230, 1470, 1750]

r7_bins = [18, 22, 26, 30, 36, 44, 52, 62, 74, 86, 100, 120, 150, 180, 210, 250, 300, 360, 420, 500,
                      600, 720, 860, 1020, 1220, 1460, 1740, 2060, 2460, 2940, 3500]

# mean_columns are those by which to group the data to get the mean
mean_columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse',
                'Traverse Speed', 'Meas Distance']

# Get only data columns needed for analysis
sympatec = sympatec[columns].reset_index(drop=True)

# Look at results from each measurement method by nozzle type
# Get list of unique nozzle types
nozzle_types = sympatec['Nozzle'].unique().tolist()

'''
For each nozzle type, assume their are two measurement methods, full traverse and spot measurements.

For the full traverse, there are two airspeeds and two traverse speeds.

For the spot measurements, there are spot measurements every inch at one airspeed.
NOTE: I need to redo this data with measurements every inch at both airspeeds (2 and 18 mph).

First, look at the full traverse data.
'''

# Get new dataframe for a specific nozzle type
nozzle_index = 4
nozzle_type = nozzle_types[nozzle_index]
nozzle_type_data = sympatec[sympatec['Nozzle'] == nozzle_type].reset_index(drop=True)

# Get Full traverse data
full_traverse_data = sliceFullTraverse(nozzle_type_data)

# Get the mean data for full traverse dataframe
full_traverse_mean_data = getMeanData(full_traverse_data, mean_columns)

# get list of unique combinations of airspeed, pressure, and traverse speed
full_traverse_mean_data['Unique'] = full_traverse_mean_data['Airspeed'].astype(str) + '_' + \
                                    full_traverse_mean_data['Pressure'].astype(str) + '_' + \
                                    full_traverse_mean_data['Traverse Speed'].astype(str)

# Compare Full traverse results using bar plot of dv10, dv50, and dv90
fig = plt.figure(figsize=(10,10), constrained_layout=True)
gs = GridSpec(ncols=1, nrows=1, figure=fig)

ax = fig.add_subplot(gs[0, 0])

# Get length of full_traverse_mean_data
length = len(full_traverse_mean_data)
bar_width = 0.1
incrementer = create_incrementer_list(length, bar_width)

# iterate through all rows in full_traverse_mean_data
for index, row in full_traverse_mean_data.iterrows():
    # Get the unique identifier for this row
    unique = row['Unique']
    # Get the data for this row
    data = row[['DV10', 'DV50', 'DV90']].values
    # Get the x locations for this row as the values 10, 50, and 90
    x = np.array([0, 1, 2])
    # Get the width of the bars
    x_values = x + incrementer[index]
    # Plot the data
    ax.bar(x_values, data, bar_width, label=unique)

# Add labels and legend
ax.set_ylabel('Diameter (um)')
ax.set_xlabel('Percentile')
ax.set_title('Comparison of Full Traverse Results for ' + str(nozzle_type))
ax.set_xticks(x)
ax.set_xticklabels(['DV10', 'DV50', 'DV90'])
ax.legend()

# Show the figure
fig.show()












