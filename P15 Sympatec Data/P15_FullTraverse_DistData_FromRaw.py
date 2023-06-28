#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 07:02:09 2021

@author: bradfritz1
"""

import pandas as pd
import numpy as np
from csv import reader
import matplotlib.pyplot as plt
import math
import glob
import re

# Pickle file with Full traverse data results from VisiSize Software
# Will be used to determine Traverse Speed by Rep
VZPickleFileName = 'AllNozzleTraverseData.pkl'
VZData = pd.read_pickle(VZPickleFileName)


ProbeVol = 3424

P15FullTravAllData = pd.DataFrame()

def StartStopKeys(filename): 
    
    # Test parameter keys to record data parameters
    StartKey = 'OXFORD LASER IMAGING SYSTEMS'
    StopKey = 'Frame	Particle ID	Diameter	Velocity	Angle	Shape Factor'
    
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

# Limited filename list for testing new code
FileNames = ['29-7-11006-Full-2.vsp']

#Read in all .vsp (Individual particle files)
#for filename in glob.iglob(r'*.vsp'):
    
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
    
    

#for filename in FileNames:
for filename in glob.iglob(r'*.vsp'):
    
    TestName = filename.replace('.vsp','')
    FileNameSort = re.split('([^a-zA-Z0-9])',TestName) # split on non alpha-numeric and keep all separators

    if FileNameSort[-3] == 'Full': # Filter out the Full Traverse datasets
    
        
        TraverseLoc = FileNameSort[-3]
        Nozzle = FileNameSort[-5]
        
        if FileNameSort[1] == '.':
            Rep = float(FileNameSort[4])
        else:
            Rep = float(FileNameSort[2])
            
        TravSpeed = VZData.loc[ (VZData['Nozzle'] == Nozzle) 
                               & (VZData['Rep'] == Rep) ]['Traverse Speed (in/min)'].values[0]
        
        userDf = pd.read_csv(filename, delim_whitespace=True,
                              skiprows = 9,header=None)

        Columns = ['Frame','Particle ID','Diameter','Velocity','Angle','Shape Factor']
    
        userDf.columns = Columns
   
        binz = np.linspace(userDf['Diameter'].min()-1,userDf['Diameter'].max()+1,200)
     
        QuantData, bins = pd.cut(userDf['Diameter'], binz, right=False, retbins=True)
        
        BinData = userDf.groupby(QuantData)['Diameter'].agg(['count'])
        BinData['Bins'] = BinData.index
        
        VelBinData = userDf.groupby(QuantData)['Velocity'].agg(['sum'])
        BinData['VelSum'] = VelBinData['sum']
        BinData['AvgBinVel'] = BinData['VelSum']/BinData['count']
    
        BinData['BinCent'] = BinData['Bins'].apply(lambda x: x.mid)
        BinData = BinData.reset_index()
    
        MidBins = pd.DataFrame(columns=['MidBin'])
    
        for i in range(0,len(bins)-1):
            MidPoint = (binz[i]+binz[i+1])/2
            BinCurrent = pd.DataFrame({'MidBin':[MidPoint]})
            MidBins = MidBins.append(BinCurrent, ignore_index = True)
        
        BinData = BinData.join(MidBins)
    
        BinData['VolWeight'] = (BinData['count']*(BinData['MidBin']**3))
        BinData['IncVolFrac'] = BinData['VolWeight'] / BinData['VolWeight'].sum()
        BinData['CumVolFrac'] = BinData['IncVolFrac'].cumsum()
        
        BinData['VolVelWeight'] = (BinData['count']*(BinData['MidBin']**3) *
                                   BinData['AvgBinVel'])
        BinData['IncVolVelFrac'] = BinData['VolVelWeight'] / BinData['VolVelWeight'].sum()
        BinData['CumVolVelFrac'] = BinData['IncVolVelFrac'].cumsum()
        BinData = BinData.replace(np.nan, 0)
        BinData = BinData[BinData['count'] != 0].reset_index()
        
        DV10, DV50, DV90 = LinearExtrapolateVolDia(BinData, 'CumVolFrac','MidBin', 0.1, 0.5, 0.9)
        DV_Vel10, DV_Vel50, DV_Vel90 = LinearExtrapolateVolDia(BinData, 'CumVolVelFrac','MidBin', 0.1, 0.5, 0.9)
        
        NumDrops = BinData['count'].sum()
        
        P15FullTravData = pd.DataFrame({'Testname':[TestName], 'Rep':[Rep],
                                        'Nozzle':[Nozzle],'TraverseLoc':TraverseLoc,
                                        'Traverse Speed (in/min)':[TravSpeed],
                                        'DV10':[DV10],'DV50':[DV50],'DV90':[DV90],
                                'DV_Vel10':[DV_Vel10],'DV_Vel50':[DV_Vel50],
                                'DV_Vel90':[DV_Vel90],'NumDrops':[NumDrops]
                                      })
        P15FullTravAllData = P15FullTravAllData.append(P15FullTravData, ignore_index = True)
        
        print(TestName)
        
SummaryData = P15FullTravAllData.groupby(['Nozzle','Traverse Speed (in/min)']).mean()

PickleFileName = 'SummaryDataFullTravFromRaw.pkl'
SummaryData.to_pickle(PickleFileName)   