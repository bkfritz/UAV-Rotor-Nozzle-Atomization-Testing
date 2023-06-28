'''
Author: B K Fritz
Date: June 16, 2023
Description: Code to load and save the Sympatec data to a pickle file

'''
import pandas as pd

def readSympatecData(filename):

    df = pd.read_csv(filename, encoding='latin1')

    columns = ['Date','Time','Range','Optical Conc','Solution','Nozzle','Orientation',
                'Orifice','Pressure','Traverse','Airspeed','Traverse Speed','Meas Distance',
                'Rep','DV10','DV50','DV90','%<30um','%<50um','%<80um','%>100um',
                '%>141um','%>150um','%>200um','%>730um','Ch 1','Ch 2','Ch 3','Ch 4',
                'Ch 5','Ch 6','Ch 7','Ch 8','Ch 9','Ch 10','Ch 11','Ch 12',
                'Ch 13','Ch 14','Ch 15','Ch 16','Ch 17','Ch 18','Ch 19','Ch 20',
                'Ch 21','Ch 22','Ch 23','Ch 24','Ch 25','Ch 26','Ch 27','Ch 28',
                'Ch 29','Ch 30','Ch 31']
        
    df.columns = columns

    df['Optical Conc'] = df['Optical Conc'].str.replace('%','').astype(float)

    return df

sympatec = readSympatecData(filename = 'All Sympatec Data.txt')

# Define the data columns to keep from original data file
columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed',
           'Traverse', 'Traverse Speed', 'Meas Distance', 'DV10', 'DV50', 'DV90',
           'Optical Conc', 'Ch 1', 'Ch 2', 'Ch 3', 'Ch 4', 'Ch 5', 'Ch 6',
           'Ch 7', 'Ch 8', 'Ch 9', 'Ch 10', 'Ch 11', 'Ch 12', 'Ch 13', 'Ch 14',
           'Ch 15', 'Ch 16', 'Ch 17', 'Ch 18', 'Ch 19', 'Ch 20', 'Ch 21', 'Ch 22',
           'Ch 23', 'Ch 24', 'Ch 25', 'Ch 26', 'Ch 27', 'Ch 28', 'Ch 29', 'Ch 30',
           'Ch 31']

# The following lists define the bin diameters for each lens
r6_bin = [9, 11, 13, 15, 18, 22, 26, 31, 37, 43, 50, 60, 75, 90, 105, 120, 150, 180, 210, 250, 300,
                      360, 430, 510, 610, 730, 870, 1030, 1230, 1470, 1750]

r7_bins = [18, 22, 26, 30, 36, 44, 52, 62, 74, 86, 100, 120, 150, 180, 210, 250, 300, 360, 420, 500,
                      600, 720, 860, 1020, 1220, 1460, 1740, 2060, 2460, 2940, 3500]

# Get only data columns needed for analysis
sympatec = sympatec[columns].reset_index(drop=True)

# Rename the last 31 columns to be the bin diameters as defined by the r7_bins list
sympatec.rename(columns=dict(zip(sympatec.columns[-31:], r7_bins)), inplace=True)

# Save the data to a pickle file called 'sympatecData.pkl'
sympatec.to_pickle('sympatecData.pkl')


