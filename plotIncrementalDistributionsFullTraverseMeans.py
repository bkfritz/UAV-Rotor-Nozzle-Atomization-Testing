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

# Move Unique column to position 9 using move_column function
means = move_column(means, 'Unique', 9)

# Get list of unique nozzle types to iterate through
nozzle_types = means['Nozzle'].unique().tolist()
nozzle_type = nozzle_types[0]
df = means[means['Nozzle'] == nozzle_type].reset_index(drop=True)

# The last 31 columns contain the incremental size distribution data
# The column names for these columns as the bin sizes
# Create a list of the column names for the incremental size distribution data
diameters = means.columns[-31:].tolist()

# Compare Full traverse results by plotting incremental distributions
fig = plt.figure(figsize=(10,10), constrained_layout=True)
gs = GridSpec(ncols=1, nrows=1, figure=fig)

ax = fig.add_subplot(gs[0, 0])

# iterate through all rows in full_traverse_mean_data
for index, row in df.iterrows():
    # Get the unique identifier for this row
    unique = row['Unique']
    # Get the data for this set as a list of values from the last 31 columns
    inc_dist = row[-31:].tolist()
    # Plot the data as a line plot with the diameter values as the x values
    ax.plot(diameters, inc_dist, label=unique)

# Convert x axis to log scale
ax.set_xscale('log')

# Add labels and legend
ax.set_ylabel('% Volume')
ax.set_xlabel('Diameter (um)')
ax.set_title('Comparison of Full Traverse Results for ' + str(nozzle_type))
ax.legend()

# Show the figure
fig.show()

# # Set figure title as the nozzle type
# figtitle = 'Full Traverse Results for ' + str(nozzle_type)

# # Save the figure
# fig.savefig(figtitle + '.png', dpi=300)


