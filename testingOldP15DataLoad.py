

import pandas as pd
import numpy as np
from csv import reader
import math
import glob
import os


'''
Last Edited April 21, 2021


The following code interates through all Summary '.txt' files within a given parent folder
containing droplet size and velocity data from the Oxford P15 system.

The code assumes a standard output file format structure and key words to
identify and record test parameters

The "ParamNames" variable must be modified to fit the specified user
set test variable names use in the ViziSize Software.  These can be determined from
the output text files.

The individual functions follow, with the processing code at the end.

'''


def RepDataDetails(filename, ParamNames):
    
    '''
    This function takes in the filenames for the VisiSizer summary output
    data files.  Note that these are not the raw data files.
    
    The function uses a list of parameter names.  These are the test identifiers
    as set by the user in the Visisizer software, so the ParamNames list 
    should be adjusted accordingly.
    
    The function then passes through the input file row by row, parsing
    the string data and identifying the appropriate ParamNames, afterwhich
    the row string data is parsed and the appropriate Test identifier
    data captured and returned.
    
    Additionally, the Particles / Frame data is captured.
    
    This function was developed to work with the default VisiSizer output
    summary text file and 10 user set test identifier parameters.  
    '''
    
    TraverseParam = False
    
    for row in reader(open(filename)):
        if row:
            if len(row[0].split()) > 1:
                
                # Run (Rep) Number
                Rep = int(filename.split('-')[CountVarPositInFilename])
                
                # Test
                if (row[0].find(ParamNames[1])) == 0:
                     TestName = row[0].split()[-1].replace('"', '')
                    
                # Nozzle 
                if (row[0].find(ParamNames[2])) == 0:
                     Noz = row[0].split()[-1].replace('"', '')
                
                # Orifice 
                if (row[0].find(ParamNames[3])) == 0:
                     Orf = row[0].split()[-1].replace('"', '')
                else: Orf = ''
                
                # Pressure 
                if (row[0].find(ParamNames[4])) == 0:
                     Press = float(row[0].split()[-1].replace('"', ''))
                     
                # Orientation
                if (row[0].find(ParamNames[5])) == 0:
                     Orient = float(row[0].split()[-1].replace('"', ''))
                else: Orient = ''
                
                # Solution
                if (row[0].find(ParamNames[6])) == 0:
                     Soln = row[0].split()[-1].replace('"', '')
                
                # Traverse
                if (row[0].find(ParamNames[7])) == 0:
                    if TraverseParam == False:
                         Traverse = row[0].split()[-1].replace('"', '')
                         TraverseParam = True
                         if Traverse == 'Full':
                             Traverse = Traverse
                         else: Traverse = float(Traverse)
                         
                # Air Speed
                if (row[0].find(ParamNames[8])) == 0:
                     AS = float(row[0].split()[-1].replace('"', ''))
                     
                # Measurement Distance 
                if (row[0].find(ParamNames[9])) == 0:
                     Dist = float(row[0].split()[-1].replace('"', ''))
                     
                # Traverse Speed 
                if (row[0].find(ParamNames[10])) == 0:
                     TravSpeed = float(row[0].split()[-1].replace('"', ''))
                     
                # Particle per Frame 
                if (row[0].find(ParamNames[11])) == 0:
                     PartPerFrm = float(row[0].split()[-1].replace('"', ''))
                     

    return ([Rep,TestName, Noz, Orf, Press, Orient, Soln, Traverse, AS, Dist,
            TravSpeed, PartPerFrm])

def StartStopKeys(filename): 
    '''
    This function is used to identify the rows in the input data file
    that contain the summary cumulative distribution data.
    
    StartKey and StopKey should match the default VisiSizer output.
    '''
    # Test parameter keys to record data parameters
    start_key = 'DIAMETER (microns)'
    stop_key = 'Size-Velocity Correlation :'
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    start_line = 0
    for i, line in enumerate(lines):
        if start_key in line:
            start_line = i
            break
    
    stop_line = 0
    for i, line in enumerate(lines):
        if stop_key in line:
            stop_line = i
            break
    
    return start_line, stop_line
            
                
    Line2 = 0
    for row in reader(open(filename)):
        Line2+=1
        if row:
            if row[0] == StopKey:
                StopLine = Line2
    
    return(StartLine, StopLine)

def LinearExtrapolateVolDia(DF,CumColName,DiaColName,Frac1, Frac2, Frac3):
    '''
    Linear interpolation function to calculate user specified volume
    fraction diameters.
    '''
    
    if DF[CumColName].min() < Frac1:
        
        x1 = DF.loc[DF[CumColName]<Frac1][-1:][CumColName].values[0]
        x2 = DF.loc[DF[CumColName]>Frac1][0:][CumColName].values[0]
        y1 = DF.loc[DF[CumColName]<Frac1][-1:][DiaColName].values[0]
        y2 = DF.loc[DF[CumColName]>Frac1][0:][DiaColName].values[0]
        
        Dia1 = y1 + (Frac1 - x1)/(x2 - x1) * (y2 - y1)
    
    else: 
        Dia1 = DF[DiaColName][0]
       
    
    xx1 = DF.loc[DF[CumColName]<Frac2][-1:][CumColName].values[0]
    xx2 = DF.loc[DF[CumColName]>Frac2][0:][CumColName].values[0]
    yy1 = DF.loc[DF[CumColName]<Frac2][-1:][DiaColName].values[0]
    yy2 = DF.loc[DF[CumColName]>Frac2][0:][DiaColName].values[0]

    Dia2 = yy1 + (Frac2 - xx1)/(xx2 - xx1) * (yy2 - yy1)
    
    if DF[CumColName].max() > Frac3:
    
        xxx1 = DF.loc[DF[CumColName]<Frac3][-1:][CumColName].values[0]
        xxx2 = DF.loc[DF[CumColName]>Frac3][0:][CumColName].values[0]
        yyy1 = DF.loc[DF[CumColName]<Frac3][-1:][DiaColName].values[0]
        yyy2 = DF.loc[DF[CumColName]>Frac3][0:][DiaColName].values[0]
    
        Dia3 = yyy1 + (Frac3 - xxx1)/(xxx2 - xxx1) * (yyy2 - yyy1)
    
    else:
        Dia3 = DF[CumColName][0]
    
    return Dia1, Dia2, Dia3

def Distribution_Data_Analysis(filename):
    '''
    This function reads in the summary cumulative distribution data into 
    a Pandas dataframe.
    
    The Columns list should align to the Standard VisiSizer column headings
    for the summary distribution data.
    
    Additionally, the volume * velocity weighted distribution is determined.

    '''
    
    StartLine, StopLine = StartStopKeys(filename)

    userDf = pd.read_csv(filename, delim_whitespace=True,
                          skiprows = StartLine,header=None)
    
    SubDF = userDf[0:(StopLine-(StartLine+1))]
    
    DistDF = SubDF.replace(',','',regex=True)
    c = DistDF.select_dtypes(object).columns
    DistDF[c] = DistDF[c].apply(pd.to_numeric, errors='coerce')
    
    Columns = ['LowerBinDia','UpperBinDia','Count','ProbeVol','% Number','% Area',
                '% Vol','Cum % Vol','Vel(m/s)']
    
    DistDF.columns = Columns
    DistDF['AvgBinDia'] = (DistDF['LowerBinDia']+DistDF['UpperBinDia'])/2
    DistDF.drop(DistDF[DistDF['Count'] == 0].index, inplace=True)
    DistDF['%VolCumFrac'] = DistDF['% Vol'].cumsum()/100
    
    DistDF['BinVelVol'] = (DistDF['Count'] * 
                           DistDF['Vel(m/s)'] *
                           DistDF['AvgBinDia']**3 ) 
    
    Velocity_Weigthed_Total_Volume = DistDF['BinVelVol'].sum()
    DistDF['VelWtIncFrac'] = DistDF['BinVelVol']/Velocity_Weigthed_Total_Volume
    DistDF['VelWtCumFrac'] = DistDF['VelWtIncFrac'].cumsum()
    
    return DistDF

def TestDropsExist(filename):
    
    # open readfilename and read and print each line
    with open(filename, 'r') as readfile:
        lines = readfile.readlines()
        
    for line in lines:
        if 'Arithmetic mean' in line:
            value = line.split('\t')[1]
    
    return value

def Nozzle_Traverse_Filters(filename):
    FileNameSort = filename.split('-')
    NozSort = FileNameSort[2]
    TravSort = FileNameSort[-2]
    return NozSort, TravSort

def Distribution_Summary_Dataframe(filename, ParamNames):
    Rep,Test,Noz,Orf,Press,Orient,Soln,Traverse,AS,Dist,TravSpeed,PartPerFrm = RepDataDetails(filename, ParamNames)
    
    Distribution_Data = Distribution_Data_Analysis(filename)
    
    DV10, DV50, DV90 = LinearExtrapolateVolDia(Distribution_Data,
                                                '%VolCumFrac','AvgBinDia',0.1,0.5,0.9)
    
    DV_Vel10, DV_Vel50, DV_Vel90 = LinearExtrapolateVolDia(Distribution_Data,
                                                'VelWtCumFrac','AvgBinDia',0.1,0.5,0.9)
    
    CurrentDSD = pd.DataFrame({'Test':[Test], 'Rep':[Rep],'Nozzle':[Noz], 
                                'Orifice':[Orf], 'Pressure (psi)':[Press], 
                                'Orient':[Orient], 'Solution':[Soln],
                                'Traverse':[Traverse], 'Traverse Speed (in/min)':[TravSpeed],
                                'AirSpeed (mph)':[AS], 
                                'MeasDistance (in)':[Dist],'PartsPerFrame':[PartPerFrm],
                                'DV10':[DV10],'DV50':[DV50],'DV90':[DV90],
                                'DV_Vel10':[DV_Vel10],'DV_Vel50':[DV_Vel50],
                                'DV_Vel90':[DV_Vel90]
                                      })
    return CurrentDSD
        
def getDistributionData(filename):
    # Define your own column names
    column_names = ["Lower Diameter", "Upper Diameter", "RAW COUNT", "PROBE VOLUME", "% NUMBER", 
                    "% AREA", "% VOLUME", "CUM % VOL", "AV. SPD (m/s)"]

    start, stop = StartStopKeys(filename)

    # read data from text file into a pandas dataframe starting at start + 1 
    # and ending at stop - 1, do not use first row as column names
    df = pd.read_csv(filename, sep=',', skiprows=start+1, nrows=stop-start-1,
                    header=None, index_col=False)

    # Drop last column, added because of trailing comma in text file
    df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)

    # Rename columns
    df.columns = column_names
    
    return df

#*************************************************************************

ParamNames = ['Run:', 'Test', 'Nozzle', 'Orifice', 'Pressure (psi)', 
              'Orientation', 'Solution','Traverse','Wind Speed (mph)',
              'Distance (in)','Traverse Speed','Particles / frame']
CountVarPositInFilename = 1

AllData = pd.DataFrame()

TraverseFilter = 'Full'
PickleFileName = 'AllNozzleTraverseData.pkl'

# DataFrame Pickle Exists?

DataPickle = False
#DataPickle = True

filename = '14.5-20-6515-Full-2.txt'

# set folder directory containing data files
directory = 'P15 Sympatec Data/'

readfilename = os.path.join(directory, filename)

# drop_count is used to ensure that drops were measured before getting the data
drop_count = TestDropsExist(readfilename)

# getDistributionData returns a dataframe with the summary data for the given measurement
df = getDistributionData(readfilename)

# Get the details of the measurement
details = RepDataDetails(readfilename, ParamNames)

# open readfilename and read and print each line
with open(readfilename, 'r') as readfile:
    lines = readfile.readlines()
    
param_dict = {
    'Test': None,
    'Nozzle': None,
    'Orifice': None,
    'Pressure (psi)': None,
    'Orientation': None,
    'Solution': None,
    'Traverse': None,
    'Wind Speed (mph)': None,
    'Distance (in)': None,
    'Traverse Speed': None,
    'Arithmetic mean': None
}

for line in lines:
    for param in param_dict.keys():
        if param in line:
            param_dict[param] = line.split('\t')[1]

if param_dict['Aritmetic mean'] > 0:
    


# if DataPickle == True:

#     AllData = pd.read_pickle(PickleFileName)

# else:

#     for filename in glob.iglob(r'*.txt'):
#     #for filename in FileNames:
        
#         DropTest = float(Test_Drops_Exist(filename))
        
#         if DropTest > 0:
    
#             NozSort, TravSort = Nozzle_Traverse_Filters(filename)
            
#             #if NozzleFilter == NozSort and TraverseFilter != TravSort:
#             if TraverseFilter == TravSort:
    
#                 CurrentDSD = Distribution_Summary_Dataframe(filename,ParamNames)
                    
#                 AllData = AllData.append(CurrentDSD, ignore_index = True)
    
#     #AllData.to_pickle(PickleFileName)
    
# SummaryData = AllData.groupby('Nozzle').mean()
