import pandas as pd
import numpy as np
from csv import reader
import math
import glob
import re

p15_df = pd.DataFrame()

probe_vol = 3424


def StartStopKeys(filename): 
    
    # Test parameter keys to record data parameters
    start_key = 'OXFORD LASER IMAGING SYSTEMS'
    stop_key = 'Frame	Particle ID	Diameter	Velocity	Angle	Shape Factor'
    
    line1 = 0
    for row in reader(open(filename)):
        line1+=1
        if row:
            if row[0] == start_key:
                start_line = line1
                
    line2 = 0
    for row in reader(open(filename)):
        line2+=1
        if row:
            if row[0] == stop_key:
                stop_line = line2

def FrameParticleFlux(current_frame, probe_vol):
    
    particles = current_frame['Particle ID'].unique()
    particle_volume_sum = 0
    particle_count = 0
    
    for particle in particles:
        
        diameter = current_frame.loc[(current_frame['Particle ID'] == particle)]['Diameter'].iloc[0]
        particle_volume = (4/3)*math.pi*(diameter/2)**3
        particle_volume_sum = particle_volume_sum + particle_volume
        particle_count += 1
    
    flux = particle_volume_sum / probe_vol # ul / mm^3
    
    return flux, particle_count    
        
def AvgFrameFlux(filename, probe_vol):
    
    df = pd.read_csv(filename, delim_whitespace=True,
                              skiprows = 9,header=None)

    columns = ['Frame','Particle ID','Diameter','Velocity','Angle','Shape Factor']
    
    df.columns = columns
    
    frames = df['Frame'].unique()
    frame_flux_sum = 0
    particle_count_sum = 0
    
    for frame in frames:
        '''
        Go frame by frame and determine droplet volume per Probe Volume
        Probe Volume for P15 at 1X mag = 3424 mm^2
        
        Then, average the relative flux for the given spray fan location
        
        This will then be used in the flux weighted distribution
                
        '''
        
        current_frame = df.loc[(df['Frame'] == frame)]
        
        frame_flux, particle_count = FrameParticleFlux(current_frame, probe_vol)
        
        particle_count_sum = particle_count_sum + particle_count
        
        frame_flux_sum = frame_flux_sum + frame_flux
        
    average_frame_flux = frame_flux_sum / len(frames)
    average_particles_per_frame = particle_count_sum / len(frames)
    number_frames = len(frames)
    
    return average_frame_flux, average_particles_per_frame, number_frames