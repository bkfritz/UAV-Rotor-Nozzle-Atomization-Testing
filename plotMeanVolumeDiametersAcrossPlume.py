import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

def move_column(df, column_name, new_pos):
    # Assuming df is your DataFrame
    # column_name is the column you want to move
    # new_pos is the position to which you want to move the column
    cols = list(df.columns)
    if column_name in cols:
        cols.remove(column_name)
        cols.insert(new_pos, column_name)
        df = df[cols]
    else:
        print(f'Column "{column_name}" does not exist in DataFrame.')
    return df

# Create function that takes in all Sympatec data and returns dataframe for given nozzle and non-Full traverse
def getNozzleTraverseData(df, nozzle):
    '''
    Get the data for a specific nozzle and non-Full traverse
    '''
    data = df[(df['Nozzle'] == nozzle) &
                        (df['Traverse'] != 'Full')].reset_index(drop=True)
    
    # Convert the Traverse column to float values
    data['Traverse'] = data['Traverse'].astype(float)
    
    # Sort the dataframe by the Traverse column in ascending order
    data.sort_values(by=['Traverse'], inplace=True)
    
    return data

# mean_columns are those by which to group the data to get the mean
mean_columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse',
                'Traverse Speed', 'Meas Distance']

# Read in the data from pickle file
sympatec = pd.read_pickle('sympatecData.pkl')

# Read in patternator data from pickle file
patternator = pd.read_pickle('PattenatorData.pkl')

# Get list of unique nozzle types
nozzle_types = sympatec['Nozzle'].unique()

# Iterate through nozzle types and plot the mean volume diameters across the plume
for nozzle_type in nozzle_types:
    
    noz_df = getNozzleTraverseData(sympatec, nozzle_type)

    # Get pattenator data for first nozzle type in nozzle_types
    pat_df = patternator[(patternator['Nozzle'] == nozzle_type)].reset_index(drop=True)

    # Calculated means grouping by mean_columns
    means = noz_df.groupby(mean_columns, as_index=False).mean()

    # get Max Traverse value in means
    max_traverse = means['Traverse'].max() + 2
    # get Min Traverse value in means
    min_traverse = means['Traverse'].min() - 2

    # Get pattenator data whose locations values are between min_traverse and max_traverse
    pat_df = pat_df[(pat_df['Location (in)'] >= min_traverse) &
                    (pat_df['Location (in)'] <= max_traverse)].reset_index(drop=True)

    # In order for Optical concetration data to be plotted on the same axis as the
    # pattenator data, the Optical concetration data must be scaled to the same
    # range as the pattenator data.

    # Get max value of Flow in patternator data
    max_flow = pat_df['Flow (L/min)'].max()

    # Get max value of Optical Conc in means
    max_optical_conc = means['Optical Conc'].max()

    # Sympatec optical concentration data scaler:
    sympatec_scaler = max_flow / max_optical_conc

    # Create figure
    fig = plt.figure(figsize=(15,10), constrained_layout=True)
    gs = GridSpec(ncols=1, nrows=1, figure=fig)

    ax = fig.add_subplot(gs[0, 0])

    # Create a second axis that shares the same x-axis
    ax2 = ax.twinx()

    # Bar plot data with x = Traverse and y = DV10

    # DV90
    ax.bar(means['Traverse'], means['DV90'], width=0.25, label='Sympatec DV90')
    # DV50
    ax.bar(means['Traverse'], means['DV50'], width=0.25, label='Sympatec DV50')
    # DV10
    ax.bar(means['Traverse'], means['DV10'], width=0.25, label='Sympatec DV10')

    # Create an empty scatter plot for the Optical Concentration data
    ax.scatter([], [], marker='x', color='black', edgecolors='white', 
                label='Optical Conc')

    # Create an empty scatter plot for the patternator data
    ax.scatter([], [], marker='o', color='red', edgecolors='black',
                label='Patternator')

    # On axis 2, plot the Optical Concentration as scatter plot, with balck x's
    # surround by a white outline
    ax2.scatter(means['Traverse'], means['Optical Conc'] * sympatec_scaler, marker='x', 
                color='black', edgecolors='white', linewidths = 2.5, label='Optical Conc')

    # On axis 2, plot the patternator data as scatter plot, with red circles
    ax2.scatter(pat_df['Location (in)'], pat_df['Flow (L/min)' ], marker='o',
                color='red', edgecolors='black', linewidths=2.5, label='Patternator')


    # Add labels and legend
    ax.set_ylabel('Diameter (um)')
    ax.set_xlabel('Distance From Center Nozzle (in)')
    ax.set_title('Size Data by Plume Position for nozzle: ' + str(nozzle_type))
    # Add legend located outside of plot
    ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    # Show the figure
    fig.show()
    
    # Figure filename
    fig_filename = 'MeanVolumeDiametersAcrossPlume_' + str(nozzle_type) + '.png'
    
    # Save the figure
    fig.savefig(fig_filename, bbox_inches='tight')