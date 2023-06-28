import pandas as pd
import numpy as np
from csv import reader

filename = 'All Sympatec Data.txt'

userDf = pd.read_csv(filename, encoding='latin1')

Columns = ['Date','Time','Range','Optical Conc','Solution','Nozzle','Orientation',
            'Orifice','Pressure','Traverse','Airspeed','Traverse Speed','Meas Distance',
            'Rep','DV10','DV50','DV90','%<30um','%<50um','%<80um','%>100um',
            '%>141um','%>150um','%>200um','%>730um','Ch 1','Ch 2','Ch 3','Ch 4',
            'Ch 5','Ch 6','Ch 7','Ch 8','Ch 9','Ch 10','Ch 11','Ch 12',
            'Ch 13','Ch 14','Ch 15','Ch 16','Ch 17','Ch 18','Ch 19','Ch 20',
            'Ch 21','Ch 22','Ch 23','Ch 24','Ch 25','Ch 26','Ch 27','Ch 28',
            'Ch 29','Ch 30','Ch 31']
    
userDf.columns = Columns

userDf['Optical Conc'] = userDf['Optical Conc'].str.replace('%','').astype(float)

FullTraverseSymptecData = userDf.loc[(userDf['Traverse'] == 'Full')].reset_index()
MeanFullTravSympatec = FullTraverseSymptecData.groupby(['Nozzle',
                                                        'Traverse Speed',
                                                        'Airspeed',
                                                        'Pressure'], as_index=False).mean()

TravLocationSympatecData = userDf.loc[(userDf['Traverse'] != 'Full')].reset_index()
MeanTravLocationSympatec = TravLocationSympatecData.groupby(['Nozzle','Traverse','Airspeed'], as_index=False).mean()
MeanTravLocationSympatec['Traverse'] = MeanTravLocationSympatec['Traverse'].astype(float)



FullTraversePickleFile = 'FullTraverseSympatecPickle.pkl'
LocTraversePickleFile = 'LocationTravSympatecPickle.pkl'

MeanFullTravSympatec.to_pickle(FullTraversePickleFile)

MeanTravLocationSympatec.to_pickle(LocTraversePickleFile)



