import xarray as xr
import numpy as np
import pandas as pd
import os

#make file readable by xarray
os.system('ncrename -v z,z_coord -v zi,zi_coord result.nc resultxr.nc')
#model output file
ncname = 'resultxr.nc'
#threshold to consider species extincted
threshold = 9.6e-3
threshold = 1.0e-4

#analysis output files
#divide in surface and deep layers and seasonal, year
ncname_surface_summer = 'result_surface_summer.nc'
ncname_surface_winter = 'result_surface_winter.nc'
ncname_surface_year = 'result_surface_year.nc'

ncname_deep_summer = 'result_deep_summer.nc'
ncname_deep_winter = 'result_deep_winter.nc'
ncname_deep_year = 'result_deep_year.nc'


ds = xr.open_dataset(ncname)

time = pd.DatetimeIndex(ds['time'].values) #dim: time
depth = ds['z_coord'].values[:,:,0,0] #dim: time,depth,lat,lon

# load variable names for bacteria, phytoplankton and zooplankton 
# lenght of varname is smaller than 10 to do not include some diagnostic variables
B = [varname for varname in ds.data_vars if 'B' in varname and '_c' in varname and len(varname) < 10]
P = [varname for varname in ds.data_vars if 'P' in varname and '_c' in varname and len(varname) < 10]
Z = [varname for varname in ds.data_vars if 'Z' in varname and '_c' in varname and len(varname) < 10]

#define a map to select depths between 0 and 10m
surface_map = np.where((depth[0] <= 0) & (depth[0] >= -10))[0]
#define a mapt to select depths between 10 and 100m
deep_map = np.where((depth[0] <= -10) & (depth[0] >= -100))[0]

print(np.shape(P))
print(np.shape(Z))

#define a map to select values in winter (january, february and march)
#time has datatype datetime64[ns]

winter_map = np.where((time.month == 1) | (time.month == 2) | (time.month == 3))[0]
summer_map = np.where((time.month == 7) | (time.month == 8) | (time.month == 9))[0]

## SURFACE
#initialize arrays with the desired shape
#seasonal datasets
B_surface_summer = np.zeros((len(B), len(summer_map), len(surface_map)))
B_surface_winter = np.zeros((len(B), len(winter_map), len(surface_map)))

P_surface_summer = np.zeros((len(P), len(summer_map), len(surface_map)))
P_surface_winter = np.zeros((len(P), len(winter_map), len(surface_map)))

Z_surface_summer = np.zeros((len(Z), len(summer_map), len(surface_map)))   
Z_surface_winter = np.zeros((len(Z), len(winter_map), len(surface_map)))

TOT_surface_summer = np.zeros((len(B)+len(P)+len(Z), len(summer_map), len(surface_map)))
TOT_surface_winter = np.zeros((len(B)+len(P)+len(Z), len(winter_map), len(surface_map)))

#full year datasets
B_surface_year = np.zeros((len(B), np.shape(depth)[0], len(surface_map)))
P_surface_year = np.zeros((len(P), np.shape(depth)[0], len(surface_map)))
Z_surface_year = np.zeros((len(Z), np.shape(depth)[0], len(surface_map)))
TOT_surface_year = np.zeros((len(B)+len(P)+len(Z), np.shape(depth)[0], len(surface_map)))

for i in range(len(B)):
    B_surface_summer[i,:,:] = ds[B[i]].values[summer_map, :, 0, 0][:, surface_map]
    B_surface_winter[i,:,:] = ds[B[i]].values[winter_map, :, 0, 0][:, surface_map]
    B_surface_year[i,:,:] = ds[B[i]].values[:, :, 0, 0][:, surface_map]

for i in range(len(P)):
    P_surface_summer[i,:,:] = ds[P[i]].values[summer_map, :, 0, 0][:, surface_map]
    P_surface_winter[i,:,:] = ds[P[i]].values[winter_map, :, 0, 0][:, surface_map]
    P_surface_year[i,:,:] = ds[P[i]].values[:, :, 0, 0][:, surface_map]

for i in range(len(Z)):
    Z_surface_summer[i,:,:] = ds[Z[i]].values[summer_map, :, 0, 0][:, surface_map]
    Z_surface_winter[i,:,:] = ds[Z[i]].values[winter_map, :, 0, 0][:, surface_map]
    Z_surface_year[i,:,:] = ds[Z[i]].values[:, :, 0, 0][:, surface_map]

#subtitute with NaN values when species cannot be observed (values < 1.e-4), i.e. can considere extincted
B_surface_summer[B_surface_summer < threshold] = np.nan
B_surface_winter[B_surface_winter < threshold] = np.nan
B_surface_year[B_surface_year < threshold] = np.nan
P_surface_summer[P_surface_summer < threshold] = np.nan
P_surface_winter[P_surface_winter < threshold] = np.nan
P_surface_year[P_surface_year < threshold] = np.nan
Z_surface_summer[Z_surface_summer < threshold] = np.nan
Z_surface_winter[Z_surface_winter < threshold] = np.nan
Z_surface_year[Z_surface_year < threshold] = np.nan

TOT_surface_summer = np.concatenate((B_surface_summer, P_surface_summer, Z_surface_summer), axis=0)
TOT_surface_winter = np.concatenate((B_surface_winter, P_surface_winter, Z_surface_winter), axis=0)
TOT_surface_year = np.concatenate((B_surface_year, P_surface_year, Z_surface_year), axis=0)


## DEEP
#initialize arrays with the desired shape
#seasonal datasets
B_deep_summer = np.zeros((len(B), len(summer_map), len(deep_map)))
B_deep_winter = np.zeros((len(B), len(winter_map), len(deep_map)))

P_deep_summer = np.zeros((len(P), len(summer_map), len(deep_map)))
P_deep_winter = np.zeros((len(P), len(winter_map), len(deep_map)))

Z_deep_summer = np.zeros((len(Z), len(summer_map), len(deep_map)))
Z_deep_winter = np.zeros((len(Z), len(winter_map), len(deep_map)))

TOT_deep_summer = np.zeros((len(B)+len(P)+len(Z), len(summer_map), len(deep_map)))
TOT_deep_winter = np.zeros((len(B)+len(P)+len(Z), len(winter_map), len(deep_map)))

#full year datasets
B_deep_year = np.zeros((len(B), np.shape(depth)[0], len(deep_map)))
P_deep_year = np.zeros((len(P), np.shape(depth)[0], len(deep_map)))
Z_deep_year = np.zeros((len(Z), np.shape(depth)[0], len(deep_map)))
TOT_deep_year = np.zeros((len(B)+len(P)+len(Z), np.shape(depth)[0], len(deep_map)))

for i in range(len(B)):
    B_deep_summer[i,:,:] = ds[B[i]].values[summer_map, :, 0, 0][:, deep_map]
    B_deep_winter[i,:,:] = ds[B[i]].values[winter_map, :, 0, 0][:, deep_map]
    B_deep_year[i,:,:] = ds[B[i]].values[:, :, 0, 0][:, deep_map]

for i in range(len(P)):
    P_deep_summer[i,:,:] = ds[P[i]].values[summer_map, :, 0, 0][:, deep_map]
    P_deep_winter[i,:,:] = ds[P[i]].values[winter_map, :, 0, 0][:, deep_map]
    P_deep_year[i,:,:] = ds[P[i]].values[:, :, 0, 0][:, deep_map]

for i in range(len(Z)):
    Z_deep_summer[i,:,:] = ds[Z[i]].values[summer_map, :, 0, 0][:, deep_map]
    Z_deep_winter[i,:,:] = ds[Z[i]].values[winter_map, :, 0, 0][:, deep_map]
    Z_deep_year[i,:,:] = ds[Z[i]].values[:, :, 0, 0][:, deep_map]

#subtitute with NaN values when species cannot be observed (values < 1.e-4), i.e. can considere extincted

B_deep_summer[B_deep_summer < threshold] = np.nan
B_deep_winter[B_deep_winter < threshold] = np.nan
B_deep_year[B_deep_year < threshold] = np.nan
P_deep_summer[P_deep_summer < threshold] = np.nan
P_deep_winter[P_deep_winter < threshold] = np.nan
P_deep_year[P_deep_year < threshold] = np.nan
Z_deep_summer[Z_deep_summer < threshold] = np.nan
Z_deep_winter[Z_deep_winter < threshold] = np.nan
Z_deep_year[Z_deep_year < threshold] = np.nan


TOT_deep_summer = np.concatenate((B_deep_summer, P_deep_summer, Z_deep_summer), axis=0)
TOT_deep_winter = np.concatenate((B_deep_winter, P_deep_winter, Z_deep_winter), axis=0)
TOT_deep_year = np.concatenate((B_deep_year, P_deep_year, Z_deep_year), axis=0)

#save the datasets
ds_surface_summer = xr.Dataset({'B': (['numB', 'time', 'depth'], B_surface_summer),
                             'P': (['numP', 'time', 'depth'], P_surface_summer),
                             'Z': (['numZ', 'time', 'depth'], Z_surface_summer),
                             'TOT': (['numBPZ', 'time', 'depth'], TOT_surface_summer),
                             'speciesB': (['numB'], B),
                             'speciesP': (['numP'], P),
                             'speciesZ': (['numZ'], Z),
                             'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                             },
                            coords={'time': time[summer_map], 'depth': depth[0, surface_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                            )
ds_surface_summer.to_netcdf(ncname_surface_summer)

ds_surface_winter = xr.Dataset({'B': (['numB', 'time', 'depth'], B_surface_winter),
                                'P': (['numP', 'time', 'depth'], P_surface_winter),
                                'Z': (['numZ', 'time', 'depth'], Z_surface_winter),
                                'TOT': (['numBPZ', 'time', 'depth'], TOT_surface_winter),
                                'speciesB': (['numB'], B),
                                'speciesP': (['numP'], P),
                                'speciesZ': (['numZ'], Z),
                                'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                                },
                                coords={'time': time[winter_map], 'depth': depth[0, surface_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                                )
ds_surface_winter.to_netcdf(ncname_surface_winter)

ds_surface_year = xr.Dataset({'B': (['numB', 'time', 'depth'], B_surface_year),
                                'P': (['numP', 'time', 'depth'], P_surface_year),
                                'Z': (['numZ', 'time', 'depth'], Z_surface_year),
                                'TOT': (['numBPZ', 'time', 'depth'], TOT_surface_year),
                                'speciesB': (['numB'], B),
                                'speciesP': (['numP'], P),
                                'speciesZ': (['numZ'], Z),
                                'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                                },
                                coords={'time': time, 'depth': depth[0, surface_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                                )
ds_surface_year.to_netcdf(ncname_surface_year)

ds_deep_summer = xr.Dataset({'B': (['numB', 'time', 'depth'], B_deep_summer),
                                'P': (['numP', 'time', 'depth'], P_deep_summer),
                                'Z': (['numZ', 'time', 'depth'], Z_deep_summer),
                                'TOT': (['numBPZ', 'time', 'depth'], TOT_deep_summer),
                                'speciesB': (['numB'], B),
                                'speciesP': (['numP'], P),
                                'speciesZ': (['numZ'], Z),
                                'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                                },
                                coords={'time': time[summer_map], 'depth': depth[0, deep_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                                )
ds_deep_summer.to_netcdf(ncname_deep_summer)

ds_deep_winter = xr.Dataset({'B': (['numB', 'time', 'depth'], B_deep_winter),
                                'P': (['numP', 'time', 'depth'], P_deep_winter),
                                'Z': (['numZ', 'time', 'depth'], Z_deep_winter),
                                'TOT': (['numBPZ', 'time', 'depth'], TOT_deep_winter),
                                'speciesB': (['numB'], B),
                                'speciesP': (['numP'], P),
                                'speciesZ': (['numZ'], Z),
                                'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                                },
                                coords={'time': time[winter_map], 'depth': depth[0, deep_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                                )
ds_deep_winter.to_netcdf(ncname_deep_winter)

ds_deep_year = xr.Dataset({'B': (['numB', 'time', 'depth'], B_deep_year),
                                'P': (['numP', 'time', 'depth'], P_deep_year),
                                'Z': (['numZ', 'time', 'depth'], Z_deep_year),
                                'TOT': (['numBPZ', 'time', 'depth'], TOT_deep_year),
                                'speciesB': (['numB'], B),
                                'speciesP': (['numP'], P),
                                'speciesZ': (['numZ'], Z),
                                'species': (['numBPZ'], np.concatenate((B, P, Z), axis=0))
                                },
                                coords={'time': time, 'depth': depth[0, deep_map], 'numB': np.arange(len(B)), 'numP': np.arange(len(P)), 'numZ': np.arange(len(Z)), 'numBPZ': np.arange(len(B)+len(P)+len(Z))},
                                )
ds_deep_year.to_netcdf(ncname_deep_year)


#close the datasets
ds.close()
