

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.legend import Legend

#from scipy.stats import binned_statistic

'''
Last Edited April 21, 2021


'''

FluxPickleFileName = 'FrameFluxData.pkl'
FluxData = pd.read_pickle(FluxPickleFileName)

DSDPickleFileName = 'AllNozzleTravPositionData.pkl'
DSDData = pd.read_pickle(DSDPickleFileName)

PattenatorPickleFileName = 'PattenatorData.pkl'
PattenatorData = pd.read_pickle(PattenatorPickleFileName) 
PattenatorData['Nozzle'] = PattenatorData['Nozzle'].astype(str)
PattenatorData.rename(columns={'Location (in)':'Traverse'}, inplace=True)

FullTraversePickleFile = 'FullTraverseSympatecPickle.pkl'
LocTraversePickleFile = 'LocationTravSympatecPickle.pkl'
Sympatec = pd.read_pickle(LocTraversePickleFile)
Sympatec['Nozzle'] = Sympatec['Nozzle'].astype(str)

AllData = pd.merge(DSDData, FluxData, on=['Nozzle', 'Traverse'])

AllData = pd.merge(AllData, PattenatorData, on=['Nozzle','Traverse'])

P15FullTravPickleFile = 'AllNozzleTraverseData.pkl'
P15FullTravData = pd.read_pickle(P15FullTravPickleFile)

MeanP15FullTraverse = P15FullTravData.groupby(['Nozzle'], as_index=False).mean()
SymFullTraverse = pd.read_pickle(FullTraversePickleFile)
MeanSymFullTraverse = SymFullTraverse.groupby(['Nozzle'], as_index=False).mean()
MeanSymFullTraverse['Nozzle'] = MeanSymFullTraverse['Nozzle'].astype(str)


Avg = MeanSymFullTraverse.loc[(MeanSymFullTraverse['Nozzle'] == '11001')]
AvgTest = Avg['DV10'].reset_index(drop=True)[0]

'''
The VisiSizer software depth of field (DOF) correction is desgined to
counter the bias toward counting more bigger droplets as they are more likely
to be in focus.  To that end it is assumed that the effect is roughly 
proportional to the diameter of the droplet.  As such, to correct for this, the
software divides the total number of droplets by the diameter.  

To attempt to adjust the relative flux, two "corrections" are made here.
1. Multiply the AvgFrameFlux X AvgPartsPerFrame
2. Multiply the AvgFrameFlux X DV50 (non Velocity Weighted)

Initially testing seems to indicate that multiplying by AvgPartsPerFrame shows
good correlation to the Pattenator measured flux.

'''

AllData['FluxPartNumCorr'] = AllData['AvgFrameFlux']*AllData['AvgPartsPerFrame']
AllData['FluxD50Corr'] = AllData['AvgFrameFlux']*AllData['DV50']

def Patt_Plot(DFmain,Nozzle,TravHead, D10Head, D50Head, D90Head, FrFluxHead,
              FlowHead, SymDF, OptCHead, markerS, MeanP15, MeanSym,
              xlabel, ylabel, slabel, Title, LegendOn, ax=None, **plt_kwargs):
    
    DF = DFmain.loc[(DFmain['Nozzle'] == Nozzle)]
    Sym = SymDF.loc[(SymDF['Nozzle'] == Nozzle)]
    Scaler1 = DF[FrFluxHead].max()/DF[FlowHead].max()
    Scaler2 = Sym[OptCHead].max()/DF[FlowHead].max()
    
    P15Avg = MeanP15.loc[(MeanP15['Nozzle'] == Nozzle)].reset_index(drop=True)
    SymAvg = MeanSym.loc[(MeanSym['Nozzle'] == Nozzle)].reset_index(drop=True)
    
    P15D10 = round(P15Avg[D10Head][0],1)
    P15D50 = round(P15Avg[D50Head][0],1)
    P15D90 = round(P15Avg[D90Head][0],1)
    
    S15D10 = round(SymAvg[D10Head][0],1)
    S15D50 = round(SymAvg[D50Head][0],1)
    S15D90 = round(SymAvg[D90Head][0],1)
    
    
    if ax is None:
        ax = plt.gca()
        
    width = 0.4

    ax.bar(DF[TravHead]-0.55*width,DF[D90Head], width, color='r', label='P15 DV90')
    ax.bar(DF[TravHead]-0.55*width,DF[D50Head], width, color='c', label='P15 DV50')
    ax.bar(DF[TravHead]-0.55*width,DF[D10Head], width, color='b', label='P15 DV10')
    
    ax.bar(Sym[TravHead]+0.55*width,Sym[D90Head],width, color='black', label='Sympatec DV90')
    ax.bar(Sym[TravHead]+0.55*width,Sym[D50Head],width, color='silver', label='Sympatec DV50')
    ax.bar(Sym[TravHead]+0.55*width,Sym[D10Head],width, color='darkslategray', label='Sympatec DV10')
    
    
    ax.text(-19, 1350, 'FULL Traverse Measurement Data', fontsize=18)
    ax.text(-19, 1300, 'P15: D10, D50, D90 = '+str(P15D10)+', '+str(P15D50)+', '+str(P15D90),
            fontsize=16)
    
    ax.text(-19, 1250, 'Sympatec: D10, D50, D90 = '+str(S15D10)+', '+str(S15D50)+', '+str(S15D90),
            fontsize=16)
    
    
    
    if xlabel == True:
        ax.set_xlabel('Distance from Center Nozzle (in)')
    if ylabel == True:
        ax.set_ylabel('Volume Diameter (\u03BCm)')

    ax.set_title(Title)
    ax.set_xlim(-20,20)
    ax.set_ylim(0,1400)
    
    ax11 = ax.twinx()
    ax11.scatter(DF[TravHead], DF[FrFluxHead]/Scaler1, c='black', 
                 marker = 'P', s=markerS, linewidths = 0.5, 
                 edgecolors = 'lightgray', label = 'Relative Flux')
    ax11.scatter(DF[TravHead], DF[FlowHead], c='blue',
                 marker = 'X', s=markerS, linewidths = 0.5, 
                 edgecolors = 'lightgray', label = 'Pattenator (L/min)')
    ax11.scatter(Sym[TravHead], Sym[OptCHead]/Scaler2, c='navy',
                 marker = 'o', s=markerS, linewidths = 0.5, 
                 edgecolors = 'lightgray', label = 'Sympatec Optical Conc')
    if slabel == True:
        ax11.set_ylabel('Flow Measurement')
    
    if LegendOn == True:
        ax.legend()
        ax11.legend()
        
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax11.get_legend_handles_labels()
                
        # ax.set_ylim([ymin, ymax])
        # ax.set_xlim([xmin, xmax])
        
    return ax, h1, l1, h2, l2
        
        


# fig = plt.figure(figsize=(20,10),constrained_layout=True)
# gs = GridSpec(ncols=3, nrows=2, figure=fig)

# ax1 = fig.add_subplot(gs[0,0])
# ax2 = fig.add_subplot(gs[0,1])
# ax3 = fig.add_subplot(gs[0,2])
# ax4 = fig.add_subplot(gs[1,0])
# ax5 = fig.add_subplot(gs[1,1])
# ax6 = fig.add_subplot(gs[1,2])

# ax1 = Patt_Plot(AllData,'11001','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, False, True, False, 'VF_F', False, ax=ax1)

# ax2 = Patt_Plot(AllData,'11003','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, False, False, False, 'F_M', False, ax=ax2)

# ax3 = Patt_Plot(AllData,'11006','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, False, False, True, 'M_C', False, ax=ax3)

# ax4 = Patt_Plot(AllData,'8008','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, True, True, False, 'C_VC', False, ax=ax4)

# ax5 = Patt_Plot(AllData,'6510','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, True, False, False, 'VC_XV', False, ax=ax5)

# ax6, h1, l1, h2, l2 = Patt_Plot(AllData,'6515','Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
#                 'Flow (L/min)', Sympatec, 'Optical Conc', 2, True, False, True, 'XC_UC', False, ax=ax6)

# fig.legend(h1, l1, loc='lower left')

# leg = Legend(fig, h2, l2, loc = 'lower right')
# fig.add_artist(leg)

# plt.subplots_adjust(bottom=0.1)

# fig.suptitle('Reference Nozzle Droplet Size and Flow Data by Fan Position')

# fig.show()

'''
Or, to plot as single plots by nozzle, uncomment below and use.
'''

Nozzles = AllData['Nozzle'].unique()
for Nozzle in Nozzles:

    fig = plt.figure(figsize=(20,10),constrained_layout=True)
    gs = GridSpec(ncols=1, nrows=1, figure=fig)
    
    ax = fig.add_subplot(gs[0,0])
    
    ax, h1, l1, h2, l2 = Patt_Plot(AllData,Nozzle,'Traverse','DV10','DV50','DV90', 'FluxPartNumCorr',
                    'Flow (L/min)', Sympatec, 'Optical Conc', 80, 
                    MeanP15FullTraverse, MeanSymFullTraverse, True, True, True, 'XC_UC', False, ax=ax)
    
    
    fig.legend(h1, l1, loc='lower left')
    
    leg = Legend(fig, h2, l2, loc = 'lower right')
    fig.add_artist(leg)
    
    plt.subplots_adjust(bottom=0.1)
    
    fig.suptitle('Reference Nozzle: ' +Nozzle+ ' Droplet Size and Flow Data by Fan Position')
    
    fig.show()
    
    figtitle = Nozzle+'.pdf'
    
    fig.savefig(figtitle, format='pdf', dpi=1000)


