import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec


# mean_columns are those by which to group the data to get the mean
mean_columns = ['Range', 'Solution', 'Nozzle', 'Orifice', 'Pressure', 'Airspeed', 'Traverse',
                'Traverse Speed', 'Meas Distance']

# Read in the data from pickle file
sympatec = pd.read_pickle('sympatecData.pkl')

# Slice out full traverse data
full_traverse_data = sympatec[sympatec['Traverse'] == 'Full'].reset_index(drop=True)

# Calculated means grouping by mean_columns
means = full_traverse_data.groupby(mean_columns, as_index=False).mean()

# Add column with combination of nozzle, airspeed, pressure, and traverse speed for labels
means['Unique'] = means['Nozzle'].astype(str) + '_' + \
    means['Airspeed'].astype(str) + '_' + \
        means['Pressure'].astype(str) + '_' + \
            means['Traverse Speed'].astype(str)

# Plot mean data for each nozzle type

# Get list of unique nozzle types to iterate through
nozzle_types = means['Nozzle'].unique().tolist()

# Incrementer list creation function used to space bars in bar plot
def create_incrementer_list(length, bar_width):
    incrementer = []

    if length % 2 == 0:  # Even length
        half_length = length // 2
        incrementer = [(i - half_length + 0.5) * bar_width for i in range(length)]
    else:  # Odd length
        half_length = length // 2
        incrementer = [(i - half_length) * bar_width for i in range(length)]

    return incrementer

# Function to create bar plots of mean data for each nozzle type
def plotNozzleMeanTraverseData(df):
    # Compare Full traverse results using bar plots of dv10, dv50, and dv90
    fig = plt.figure(figsize=(10,10), constrained_layout=True)
    gs = GridSpec(ncols=1, nrows=1, figure=fig)

    ax = fig.add_subplot(gs[0, 0])

    # Get length of full_traverse_mean_data
    length = len(df)
    bar_width = 0.1
    incrementer = create_incrementer_list(length, bar_width)

    # iterate through all rows in full_traverse_mean_data
    for index, row in df.iterrows():
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

    # Set figure title as the nozzle type
    figtitle = 'Full Traverse Results for ' + str(nozzle_type)

    # Save the figure
    fig.savefig(figtitle + '.png', dpi=300)

# Iterate through nozzle types and plot mean data for each nozzle type
for nozzle_type in nozzle_types:
    # Slice out data for this nozzle type
    nozzle_type_data = means[means['Nozzle'] == nozzle_type].reset_index(drop=True)
    # Plot data and save plots
    plotNozzleMeanTraverseData(nozzle_type_data)

