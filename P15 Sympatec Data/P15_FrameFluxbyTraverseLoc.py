

import pandas as pd
import numpy as np
from csv import reader
import matplotlib.pyplot as plt
import math
import glob
import re

#from scipy.stats import binned_statistic

'''
Last Edited April 21, 2021


Analysis of the individual particle data.

'''

AllData = pd.DataFrame()


ProbeVol = 3424


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


def Frame_Particle_Flux(CurrentFrame, ProbeVol):
    
    Particles = CurrentFrame['Particle ID'].unique()
    PartVolSum = 0
    PartCount = 0
    
    for Particle in Particles:
        
        Diameter = CurrentFrame.loc[(CurrentFrame['Particle ID'] == Particle)]['Diameter'].iloc[0]
        PartVol = (4/3)*math.pi*(Diameter/2)**3
        PartVolSum = PartVolSum + PartVol
        PartCount += 1
    
    Flux = PartVolSum / ProbeVol # ul / mm^3
    
    return Flux, PartCount    
        
def Avg_Frame_Flux(filename, ProbeVol):
    
    userDf = pd.read_csv(filename, delim_whitespace=True,
                              skiprows = 9,header=None)

    Columns = ['Frame','Particle ID','Diameter','Velocity','Angle','Shape Factor']
    
    userDf.columns = Columns
    
    Frames = userDf['Frame'].unique()
    FrameFluxSum = 0
    ParticleCountSum = 0
    
    for Frame in Frames:
        '''
        Go frame by frame and determine droplet volume per Probe Volume
        Probe Volume for P15 at 1X mag = 3424 mm^2
        
        Then, average the relative flux for the given spray fan location
        
        This will then be used in the flux weighted distribution
                
        '''
        
        CurrentFrame = userDf.loc[(userDf['Frame'] == Frame)]
        
        FrameFlux, PartCount = Frame_Particle_Flux(CurrentFrame, ProbeVol)
        
        ParticleCountSum = ParticleCountSum + PartCount
        
        FrameFluxSum = FrameFluxSum + FrameFlux
        
    AvgFrameFlux = FrameFluxSum / len(Frames)
    AvgParticlesPerFrame = ParticleCountSum / len(Frames)
    NumFrames = len(Frames)
    
    return AvgFrameFlux, AvgParticlesPerFrame, NumFrames


#Read in all .vsp (Individual particle files)
for filename in glob.iglob(r'*.vsp'):
#for filename in FileNames:
    
    TestName = filename.replace('.vsp','')
    FileNameSort = re.split('([^a-zA-Z0-9])',TestName) # split on non alpha-numeric and keep all separators

    if FileNameSort[-3] != 'Full': # Filter out the Full Traverse datasets
        
        print(filename)
        
        if len(FileNameSort[-5]) > 3:  # Non-Negitive Traverse Positions
            # Nozzle Name = [-5]; Traverse Position = [-1]
        
            Nozzle = FileNameSort[-5]
            Traverse = float(FileNameSort[-3])
            #print('YES', FileNameSort, Nozzle, Traverse)
            
            AvgFrameFlux, AvgPartsPerFrame, NumFrames = Avg_Frame_Flux(filename, ProbeVol)
            
            CurrentData = pd.DataFrame({'Nozzle':[Nozzle], 'Traverse':[Traverse],
                                    'AvgFrameFlux':[AvgFrameFlux],
                                    'AvgPartsPerFrame':[AvgPartsPerFrame],
                                    'NumberOfFrames':[NumFrames]
                                      })
            AllData = AllData.append(CurrentData, ignore_index = True)
            
            
        if len(FileNameSort[-5]) < 3:  # Negitive Traverse Positions
            # Nozzle Name = [-7]; Traverse Position = [-1]

            Nozzle = FileNameSort[-7]
            Traverse = float(FileNameSort[-3])*-1
            #print('NO', FileNameSort, Nozzle, Traverse)

            AvgFrameFlux, AvgPartsPerFrame, NumFrames = Avg_Frame_Flux(filename, ProbeVol)
        
            CurrentData = pd.DataFrame({'Nozzle':[Nozzle], 'Traverse':[Traverse],
                                        'AvgFrameFlux':[AvgFrameFlux],
                                        'AvgPartsPerFrame':[AvgPartsPerFrame],
                                        'NumberOfFrames':[NumFrames]
                                          })
            AllData = AllData.append(CurrentData, ignore_index = True)
            
PickleFileName = 'FrameFluxData.pkl'
AllData.to_pickle(PickleFileName)   
        


