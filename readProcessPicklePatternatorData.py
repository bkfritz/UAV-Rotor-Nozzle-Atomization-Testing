import pandas as pd
import numpy as np


filename = '2021_Brad-Refrence.xlsx'

sheetname = 'Clean'

new_pat_df = pd.DataFrame()

patternator_df = pd.read_excel(filename, sheet_name=sheetname)

mean_df = patternator_df.groupby(['Nozzle', 'Position (in)'], as_index=False).mean()

nozzles = mean_df['Nozzle'].unique()

new_xs = np.arange(-20,21,1) 

for nozzle in nozzles:
    
    df = mean_df.loc[(mean_df['Nozzle'] == nozzle)]
    
    df_expand = pd.DataFrame()
    
    df_expand['Location (in)']=np.transpose(new_xs)
    
    # #Add extrapolated and smoothed data to the new dataframe, df_expand  
    df_expand['Flow (L/min)'] = np.interp(new_xs, df['Position (in)'], df['Flow (L/min)'])
    df_expand['Nozzle'] = nozzle

    # #Append the new dataframe, df_expand, to the new dataframe, new_pat_df
    new_pat_df = pd.concat([new_pat_df, df_expand], ignore_index=True)
    
# Replace all nan in new_pat_df with 0
new_pat_df.fillna(0, inplace=True)
    
pickle_file = 'PattenatorData.pkl'
new_pat_df.to_pickle(pickle_file) 