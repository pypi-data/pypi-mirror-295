import numpy as np
#import netCDF4 as nc
import comstabpy 
import matplotlib.pyplot as plt
import xarray as xr

#load the stability analysis module
stb = comstabpy.comstab()


ncnames = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc','result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']

#communities names: phytoplankton, zooplankton, total(B+P+Z)
communities = ['P','Z','TOT']
labels = np.array(['s_w_P','s_w_Z','s_w_TOT','s_s_P','s_s_Z','s_s_TOT','s_y_P','s_y_Z','s_y_TOT','d_w_P','d_w_Z','d_w_TOT','d_s_P','d_s_Z','d_s_TOT','d_y_P','d_y_Z','d_y_TOT'])

cvs_arr  = np.zeros((len(labels),32,4)) #32 is maximum depth layers number
stab_arr = np.zeros((len(labels),32,4))
rela_arr = np.zeros((len(labels),32,3))

meanflag = False # True if you want to compute the annual mean of the data

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    
    if meanflag:
        ds = ds.groupby('time.year').mean('time')
        time = np.array(ds['year'][:])
    else:
        time = np.array(ds['time'][:])    

    for icomm,community in enumerate(communities):
        data = np.array(ds[community])[:,:,:]

        for idepth in range(data.shape[2]):
#           print(idepth)
            try:
                #remove rows with all nan values of temporal axis of data
                mask = np.isnan(data[:,:,idepth]).all(axis=1)
                result = stb.partition(data[~mask,:,idepth],stamp=False)
                cvs_arr[inc*3+icomm,idepth]  = result['CVs']
                stab_arr[inc*3+icomm,idepth] = result['Stabilization']
                rela_arr[inc*3+icomm,idepth] = result['Relative']
            except:
                cvs_arr[inc*3+icomm,idepth]  = np.array([np.nan,np.nan,np.nan,np.nan])
                stab_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan,np.nan,np.nan])
                rela_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan,np.nan])
                continue
 
        if 'surface' in ncname:
            cvs_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan,np.nan])
            stab_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan,np.nan])
            rela_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan])
        

#Compute Tukeys HSD test

#CVs
# CVe, CVtilde, CVa, CVc   
tukey_cve = stb.Tukey(cvs_arr[:,:,0], labels=labels, savecsv=True, csvname='cve_Tukey.csv')
tukey_cvt = stb.Tukey(cvs_arr[:,:,1], labels=labels, savecsv=True, csvname='cvt_Tukey.csv')
tukey_cva = stb.Tukey(cvs_arr[:,:,2], labels=labels, savecsv=True, csvname='cva_Tukey.csv')
tukey_cvc = stb.Tukey(cvs_arr[:,:,3], labels=labels, savecsv=True, csvname='cvc_Tukey.csv')

#Stabilization
# tau, delta, psi, omega
tukey_stt = stb.Tukey(stab_arr[:,:,0], labels=labels, savecsv=True, csvname='stt_Tukey.csv')
tukey_std = stb.Tukey(stab_arr[:,:,1], labels=labels, savecsv=True, csvname='std_Tukey.csv')
tukey_stp = stb.Tukey(stab_arr[:,:,2], labels=labels, savecsv=True, csvname='stp_Tukey.csv')
tukey_sto = stb.Tukey(stab_arr[:,:,3], labels=labels, savecsv=True, csvname='sto_Tukey.csv')

#Relative
# delta_cont, psi_cont, omega_cont
tukey_red = stb.Tukey(rela_arr[:,:,0], labels=labels, savecsv=True, csvname='red_Tukey.csv')
tukey_rep = stb.Tukey(rela_arr[:,:,1], labels=labels, savecsv=True, csvname='rep_Tukey.csv')
tukey_reo = stb.Tukey(rela_arr[:,:,2], labels=labels, savecsv=True, csvname='reo_Tukey.csv')


temp = np.array(tukey_cvc)
keys = tukey_cvc.keys()
for ii in range(len(temp[:,0])):
    for jj in range(len(temp[0,:])):
        if temp[ii,jj] < 0.05:
            if jj > ii:
                print(keys[ii],keys[jj], temp[ii,jj])