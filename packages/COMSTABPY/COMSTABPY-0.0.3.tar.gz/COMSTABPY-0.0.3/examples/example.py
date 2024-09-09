import numpy as np
#import netCDF4 as nc
import comstabpy 
import matplotlib.pyplot as plt
import xarray as xr

#load the stability analysis module
stb = comstabpy.comstab()

#chose depth layer
layer = 'surface'
#layer = 'deep'

#arrays to save the rate of layers where the analysis worked correctly
winter_rate = np.zeros(3)
summer_rate = np.zeros(3)
year_rate = np.zeros(3)

#communities names: phytoplankton, zooplankton, total(B+P+Z)
communities = ['P','Z','TOT']
labels= np.array(['w_P','w_Z','w_TOT','s_P','s_Z','s_TOT','y_P','y_Z','y_TOT'])
#markers = np.array(['o','s','^','o','s','^','o','s','^'])
markers = np.array(['o','^','*','o','^','*','o','^','*'])
colors = np.array(['b','b','b','r','r','r','g','g','g'])

#surface
if layer == 'surface':
    ncnames = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc']
#deep
if layer == 'deep':
    ncnames = ['result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']
#ncnames = ['result_surface_winter.nc']


cvs_mean = np.zeros((len(ncnames),len(communities),4))
cvs_std  = np.zeros((len(ncnames),len(communities),4))

stab_mean = np.zeros((len(ncnames),len(communities),4))
stab_std  = np.zeros((len(ncnames),len(communities),4))

rela_mean = np.zeros((len(ncnames),len(communities),3))
rela_std  = np.zeros((len(ncnames),len(communities),3))

meanflag = False # True if you want to compute the annual mean of the data
#markers = ['o','s']
#labels = ['comm1','comm2']

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    #keep only the last year of ds
    #ds = ds.sel(time=slice('2009-01-01', '2009-12-31'))
    #annual mean of ds
    if meanflag:
        ds = ds.groupby('time.year').mean('time')
        time = np.array(ds['year'][:])
    else:
        time = np.array(ds['time'][:])    

    for icomm,community in enumerate(communities):
        data = np.array(ds[community])[:,:,:]

        if 'Z' in community:
            if 'summer' in ncname:  #works
                #remove rows of data with coefficient of variation > 1.0
                mask = np.zeros(data.shape,dtype=bool)
                for idp in range(data.shape[1]):
                    mask[:,idp,:] = np.nanstd(data,axis=1)/np.nanmean(data,axis=1) > 2.0
                data[mask] = np.nan
        
         #create array where to save the stability analysis    
        cvs_arr           = np.zeros((data.shape[2],4)) # CVe, CVtilde, CVa, CVc
        stabilization_arr = np.zeros((data.shape[2],4)) # tau, delta, psi, omega
        relative_arr      = np.zeros((data.shape[2],3)) # delta_cont, psi_cont, omega_cont
        count = 0
        # Run the analysis
        for idepth in range(data.shape[2]):
#           print(idepth)
            try:
                #remove rows with all nan values of temporal axis of data
                mask = np.isnan(data[:,:,idepth]).all(axis=1)
                result = stb.partition(data[~mask,:,idepth],stamp=False)
                cvs_arr[idepth]           = result['CVs']
                stabilization_arr[idepth] = result['Stabilization']
                relative_arr[idepth]      = result['Relative']
                count += 1
            except:
                cvs_arr[idepth]           = np.array([np.nan,np.nan,np.nan,np.nan])
                stabilization_arr[idepth] = np.array([np.nan,np.nan,np.nan,np.nan])
                relative_arr[idepth]      = np.array([np.nan,np.nan,np.nan])
                continue
        print(ncname,community,count/data.shape[2])
        if 'summer' in ncname:
            if 'P' in community:
                summer_rate[0]= count/data.shape[2]
            if 'Z' in community:
                summer_rate[1]= count/data.shape[2]
            if 'TOT' in community:
                summer_rate[2]= count/data.shape[2]
        if 'winter' in ncname:
            if 'P' in community:
                winter_rate[0]= count/data.shape[2]
            if 'Z' in community:
                winter_rate[1]= count/data.shape[2]
            if 'TOT' in community:
                winter_rate[2]= count/data.shape[2]
        if 'year' in ncname:
            if 'P' in community:
                year_rate[0]= count/data.shape[2]
            if 'Z' in community:
                year_rate[1]= count/data.shape[2]
            if 'TOT' in community:
                year_rate[2]= count/data.shape[2]
#        if 'winter' in ncname:
#            if 'Z' in community:
#                print(np.nanmean(cvs_arr,axis=0))
#                print(np.nanmean(stabilization_arr,axis=0))
#                print(np.nanmean(relative_arr,axis=0))
        
        cvs_mean[inc,icomm] = np.nanmean(cvs_arr,axis=0)
        cvs_std[inc,icomm]  = np.nanstd(cvs_arr,axis=0)
        stab_mean[inc,icomm] = np.nanmean(stabilization_arr,axis=0)
        stab_std[inc,icomm]  = np.nanstd(stabilization_arr,axis=0)
        rela_mean[inc,icomm] = np.nanmean(relative_arr,axis=0)
        rela_std[inc,icomm]  = np.nanstd(relative_arr,axis=0)

# cvs_mean has shape (3,3,4) i would like to tranform it in (9,4)
cvs_mean = cvs_mean.reshape((len(ncnames)*len(communities),4))
cvs_std  = cvs_std.reshape((len(ncnames)*len(communities),4))
stab_mean = stab_mean.reshape((len(ncnames)*len(communities),4))
stab_std  = stab_std.reshape((len(ncnames)*len(communities),4))
rela_mean = rela_mean.reshape((len(ncnames)*len(communities),3))
rela_std  = rela_std.reshape((len(ncnames)*len(communities),3))

print(stab_mean[2])
print(stab_std[2])
#remove rows with nan values from rela mean and std
mask = np.isnan(cvs_mean).any(axis=1)
labels = labels[~mask]
markers = markers[~mask]
colors = colors[~mask]

#Plot the results
rep = rela_mean[~mask]
arr_tau = stab_mean[~mask,0]
#rep = np.array([[0.1,0.4,0.5],[0.3,0.3,0.4]])
#arr_tau = np.array([0.2,0.7])
fig,ax = stb.ternaryplot(res=rep,tau=arr_tau,sizelegend=True,marker=markers,labels=labels,color=colors,figname=layer+'ternary.png')
fig.show()
plt.show()

#plot CVs

CVs = cvs_mean[~mask,:]
errors = cvs_std[~mask,:]

fig,ax = stb.plotCV(CV_arr=CVs,ylabel='LogScale',errorbar=errors,marker=markers,labels=labels,color=colors,figname=layer+'CVs.png')
plt.show()

effects = stab_mean[~mask,1:]
errors = stab_std[~mask,1:]
fig,ax = stb.plotEFFECT(EFF=effects,ylogscale=False,errorbar=errors,marker=markers,labels=labels,color=colors,figname=layer+'effect.png')
plt.show()


#creat cvs file with the rates of the analysis
#   | winter | summer | year |
#  P| 0.5    | 0.5    | 0.5  |
#  Z| 0.5    | 0.5    | 0.5  |
#TOT| 0.5    | 0.5    | 0.5  |
#where the values are the rate of layers where the analysis worked correctly
#the table should be saved in a csv file
import pandas as pd
dic = {'Trophic group':communities, 'Winter':winter_rate, 'Summer':summer_rate, 'Year':year_rate}

df = pd.DataFrame(dic)
df.to_csv(layer+'rates.csv',index=False)
