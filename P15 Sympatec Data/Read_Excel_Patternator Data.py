

import pandas as pd
import numpy as np
from csv import reader
import matplotlib.pyplot as plt
import math
import glob
import re
from matplotlib.gridspec import GridSpec
from scipy.interpolate import interp1d

#from scipy.stats import binned_statistic

'''
Last Edited April 21, 2021


'''
FileName = '2021_Brad-Refrence.xlsx'
SheetName = 'Clean'

PattenatorAllData = pd.DataFrame()

PattenatorData = pd.read_excel(FileName, sheet_name=SheetName)

MeanPatternData = PattenatorData.groupby(['Nozzle', 'Position (in)'], as_index=False).mean()

Nozzles = MeanPatternData['Nozzle'].unique()

NewXLocs = np.arange(-20,21,1) 

for Nozzle in Nozzles:
    
    VF_F = MeanPatternData.loc[(MeanPatternData['Nozzle'] == Nozzle)]
    
    MyDFexpand = pd.DataFrame()
    
    MyDFexpand['Location (in)']=np.transpose(NewXLocs)
    # #Add extrapolated and smoothed data to the new dataframe, MyDFexpand  
    MyDFexpand['Flow (L/min)'] = np.interp(NewXLocs,VF_F['Position (in)'],VF_F['Flow (L/min)'])
    MyDFexpand['Nozzle'] = Nozzle

    PattenatorAllData = PattenatorAllData.append(MyDFexpand)
    
PickleFileName = 'PattenatorData.pkl'
PattenatorAllData.to_pickle(PickleFileName) 