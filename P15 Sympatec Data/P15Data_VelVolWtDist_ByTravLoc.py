

import pandas as pd
import numpy as np
from csv import reader
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import math
import glob
import re

#from scipy.stats import binned_statistic

'''
Last Edited April 21, 2021


The following code interates through all '.txt' file within a given parent folder
containing droplet size and velocity data from the Oxford P15 system.

The code assumes a standard output file format structure and key words to
identify and record test parameters

The "ParamNames" variable must be modified to fit the specified user
set test variable names use in the ViziSize Software.  These can be determined from
the output text files

'''

#filename = 'Validation-Pump-12-25-12-0-0-0.txt'

# ParamNames = ['Run:', 'Test Name', 'Nozzle', 'Orifice', 'Pressure', 'Distance',
#               'Air', 'Orientation']


def RepDataDetails(filename, ParamNames):
    
    TraverseParam = False
    
    for row in reader(open(filename)):
        if row:
            if len(row[0].split()) > 1:
                
                # Run (Rep) Number
                # This code should be adjusted to reflect to location of the 
                # run number count variable in the filename
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
                     
                # Particle per Frame 
                if (row[0].find(ParamNames[10])) == 0:
                     PartPerFrm = float(row[0].split()[-1].replace('"', ''))
                     

    return (Rep,TestName, Noz, Orf, Press, Orient, Soln, Traverse, AS, Dist,PartPerFrm)

def StartStopKeys(filename): 
    
    # Test parameter keys to record data parameters
    StartKey = 'DIAMETER (microns)'
    StopKey = 'Size-Velocity Correlation :'
    
    Line1 = 0
    for row in reader(open(filename)):
        Line1+=1
        if row:
            if row[0] == StartKey:
                StartLine = Line1
                
    Line2 = 0
    for row in reader(open(filename)):
        Line2+=1
        if row:
            if row[0] == StopKey:
                StopLine = Line2
    
    return(StartLine, StopLine)

def LinearExtrapolateVolDia(DF,CumColName,DiaColName,Frac1, Frac2, Frac3):
    
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

def Test_Drops_Exist(filename):
    
    # Test if droplets were found
    for row in reader(open(filename)):
        if row:
            # Arithmetic mean
            if (row[0].find('Arithmetic mean')) == 0:
                 ArithmeticMean = row[0].split()[-1].replace('"', '')
    return ArithmeticMean

def Nozzle_Traverse_Filters(filename):
    FileNameSort = filename.split('-')
    NozSort = FileNameSort[2]
    TravSort = FileNameSort[-2]
    return NozSort, TravSort

def Distribution_Summary_Dataframe(filename, ParamNames):
    Rep,Test,Noz,Orf,Press,Orient,Soln,Traverse,AS,Dist,PartPerFrm = RepDataDetails(filename, ParamNames)
    
    Distribution_Data = Distribution_Data_Analysis(filename)
    
    DV10, DV50, DV90 = LinearExtrapolateVolDia(Distribution_Data,
                                                '%VolCumFrac','AvgBinDia',0.1,0.5,0.9)
    
    DV_Vel10, DV_Vel50, DV_Vel90 = LinearExtrapolateVolDia(Distribution_Data,
                                                'VelWtCumFrac','AvgBinDia',0.1,0.5,0.9)
    
    CurrentDSD = pd.DataFrame({'Test':[Test], 'Rep':[Rep],'Nozzle':[Noz], 
                                'Orifice':[Orf], 'Pressure (psi)':[Press], 
                                'Orient':[Orient], 'Solution':[Soln],
                                'Traverse':[Traverse],'AirSpeed (mph)':[AS], 
                                'MeasDistance (in)':[Dist],'PartsPerFrame':[PartPerFrm],
                                'DV10':[DV10],'DV50':[DV50],'DV90':[DV90],
                                'DV_Vel10':[DV_Vel10],'DV_Vel50':[DV_Vel50],
                                'DV_Vel90':[DV_Vel90]
                                      })
    return CurrentDSD
        

#*************************************************************************

ParamNames = ['Run:', 'Test', 'Nozzle', 'Orifice', 'Pressure (psi)', 
              'Orientation', 'Solution','Traverse','Wind Speed (mph)',
              'Distance (in)','Particles / frame']
CountVarPositInFilename = 1

AllData = pd.DataFrame()

TraverseFilter = 'Full'
PickleFileName = 'AllNozzleTravPositionData.pkl'

# DataFrame Pickle Exists?

DataPickle = True
Plot = True

if DataPickle == True:

    AllData = pd.read_pickle(PickleFileName)

else:

    for filename in glob.iglob(r'*.txt'):
        
        DropTest = float(Test_Drops_Exist(filename))
        
        if DropTest > 0:
    
            NozSort, TravSort = Nozzle_Traverse_Filters(filename)
            
            #if NozzleFilter == NozSort and TraverseFilter != TravSort:
            if TraverseFilter != TravSort:
    
                CurrentDSD = Distribution_Summary_Dataframe(filename,ParamNames)
                    
                AllData = AllData.append(CurrentDSD, ignore_index = True)
    
    AllData.to_pickle(PickleFileName)

if Plot == True:
        
    
    # # Get Nozzle Names
    Nozzles = AllData['Nozzle'].unique()
    
    # 11001 Data
    VF_F = AllData.loc[(AllData['Nozzle'] == '11001')]
    F_M = AllData.loc[(AllData['Nozzle'] == '11003')]
    M_C = AllData.loc[(AllData['Nozzle'] == '11006')]
    C_VC = AllData.loc[(AllData['Nozzle'] == '8008')]
    VC_XC = AllData.loc[(AllData['Nozzle'] == '6510')]
    XC_UC = AllData.loc[(AllData['Nozzle'] == '6515')]
    
    
    fig = plt.figure(figsize=(15,10),constrained_layout=True)
    gs = GridSpec(ncols=3, nrows=2, figure=fig)
    
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[0,1])
    ax3 = fig.add_subplot(gs[0,2])
    ax4 = fig.add_subplot(gs[1,0])
    ax5 = fig.add_subplot(gs[1,1])
    ax6 = fig.add_subplot(gs[1,2])
    
    ax1.bar(VF_F['Traverse'],VF_F['DV90'], label='DV90')
    ax1.bar(VF_F['Traverse'],VF_F['DV50'], label='DV50')
    ax1.bar(VF_F['Traverse'],VF_F['DV10'], label='DV10')
    
    ax1.set_xlabel('Distance from Center Nozzle (in)')
    ax1.set_ylabel('Volume Diameter')
    ax1.set_title('VF_F')
    ax1.set_xlim(-20,20)
    ax1.set_ylim(0,1200)
    ax1.legend()
    
    ax2.bar(F_M['Traverse'],F_M['DV90'], label='DV90')
    ax2.bar(F_M['Traverse'],F_M['DV50'], label='DV50')
    ax2.bar(F_M['Traverse'],F_M['DV10'], label='DV10')
    
    ax2.set_xlabel('Distance from Center Nozzle (in)')
    ax2.set_ylabel('Volume Diameter')
    ax2.set_title('F_M')
    ax2.set_xlim(-20,20)
    ax2.set_ylim(0,1200)
    ax2.legend()
    
    ax3.bar(M_C['Traverse'],M_C['DV90'], label='DV90')
    ax3.bar(M_C['Traverse'],M_C['DV50'], label='DV50')
    ax3.bar(M_C['Traverse'],M_C['DV10'], label='DV10')
    
    ax3.set_xlabel('Distance from Center Nozzle (in)')
    ax3.set_ylabel('Volume Diameter')
    ax3.set_title('M_C')
    ax3.set_xlim(-20,20)
    ax3.set_ylim(0,1200)
    ax3.legend()
    
    ax4.bar(C_VC['Traverse'],C_VC['DV90'], label='DV90')
    ax4.bar(C_VC['Traverse'],C_VC['DV50'], label='DV50')
    ax4.bar(C_VC['Traverse'],C_VC['DV10'], label='DV10')
    
    ax4.set_xlabel('Distance from Center Nozzle (in)')
    ax4.set_ylabel('Volume Diameter')
    ax4.set_title('C_VC')
    ax4.set_xlim(-20,20)
    ax4.set_ylim(0,1200)
    ax4.legend()
    
    ax5.bar(VC_XC['Traverse'],VC_XC['DV90'], label='DV90')
    ax5.bar(VC_XC['Traverse'],VC_XC['DV50'], label='DV50')
    ax5.bar(VC_XC['Traverse'],VC_XC['DV10'], label='DV10')
    
    ax5.set_xlabel('Distance from Center Nozzle (in)')
    ax5.set_ylabel('Volume Diameter')
    ax5.set_title('VC_XC')
    ax5.set_xlim(-20,20)
    ax5.set_ylim(0,1200)
    ax5.legend()
    
    ax6.bar(XC_UC['Traverse'],XC_UC['DV90'], label='DV90')
    ax6.bar(XC_UC['Traverse'],XC_UC['DV50'], label='DV50')
    ax6.bar(XC_UC['Traverse'],XC_UC['DV10'], label='DV10')
    
    ax6.set_xlabel('Distance from Center Nozzle (in)')
    ax6.set_ylabel('Volume Diameter')
    ax6.set_title('XC_UC')
    ax6.set_xlim(-20,20)
    ax6.set_ylim(0,1200)
    ax6.legend()
    
    fig.show()
