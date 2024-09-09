import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd

# Load the data
#model output file
ncname = 'resultxr.nc'
#threshold to consider species extincted
threshold = 9.6e-3
threshold = 1.0e-4

season = 'winter'
#season = 'summer'

ds = xr.open_dataset(ncname)

time = pd.DatetimeIndex(ds['time'].values) #dim: time
depth = ds['z_coord'].values[:,:,0,0] #dim: time,depth,lat,lon

# load variable names for bacteria, phytoplankton and zooplankton 
# lenght of varname is smaller than 10 to do not include some diagnostic variables
B = [varname for varname in ds.data_vars if 'B' in varname and '_c' in varname and len(varname) < 10]
P = [varname for varname in ds.data_vars if 'P' in varname and '_c' in varname and len(varname) < 10]
Z = [varname for varname in ds.data_vars if 'Z' in varname and '_c' in varname and len(varname) < 10]

winter_map = np.where((time.month == 1) | (time.month == 2) | (time.month == 3))[0]
summer_map = np.where((time.month == 7) | (time.month == 8) | (time.month == 9))[0]

B_c = np.zeros(len(depth[0,:])) #dim: depth
P_c = np.zeros(len(depth[0,:])) #dim: depth
Z_c = np.zeros(len(depth[0,:])) #dim: depth

if season == 'winter':
    for iv,vname in enumerate(B):
        B_c = B_c + np.nanmean(ds[vname].values[winter_map,:,0,0],axis=0)
    for iv,vname in enumerate(P):
        P_c = P_c + np.nanmean(ds[vname].values[winter_map,:,0,0],axis=0)
    for iv,vname in enumerate(Z):
        Z_c = Z_c + np.nanmean(ds[vname].values[winter_map,:,0,0],axis=0)

if season == 'summer':
    for iv,vname in enumerate(B):
        B_c = B_c + np.nanmean(ds[vname].values[summer_map,:,0,0],axis=0)
    for iv,vname in enumerate(P):
        P_c = P_c + np.nanmean(ds[vname].values[summer_map,:,0,0],axis=0)
    for iv,vname in enumerate(Z):
        Z_c = Z_c + np.nanmean(ds[vname].values[summer_map,:,0,0],axis=0)

# Plot the data
fig, ax = plt.subplots()

ax.plot(B_c, depth[0,:], label='Bacteria', color='k', marker='s',zorder=1)
ax.plot(P_c, depth[0,:], label='Phyto', color='k', marker='o',zorder=2)
ax.plot(Z_c, depth[0,:], label='Zoo', color='k', marker='^',zorder=3)

ax.set_xlabel('$[mgC/m^3]$')
ax.set_ylabel('Depth [m]')
ax.set_ylim(-200,0)

ax.set_title(season)

ax.legend()

#add grid of depths
#i would like to add a horizontal line for each point of depth[0,:]
for idepth in depth[0,:]:
    ax.axhline(y=idepth, color='gray', linestyle='-', linewidth=0.5, zorder=0, alpha=0.5)
#ax.grid(axis='y')

fig.savefig(season+'_column.png', dpi=600)

plt.show()
