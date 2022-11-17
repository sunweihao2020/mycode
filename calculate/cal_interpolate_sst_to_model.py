'''
2022-11-12
This code interpolate the model output SST to the inputfile SST
'''
input_file  =  '/home/sun/data/ocean_data/all_climate_monthly_means_trans.nc'
model_sst   =  '/home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c180511.nc'

import xarray as xr
import numpy as np
import scipy

f0  =  xr.open_dataset(input_file)
f1  =  xr.open_dataset(model_sst)

# ----- read lat/lon information --------
print(f0.tos.data.shape)      # (12, 458, 540)
print(f1.SST_cpl.data.shape)  # (12, 180, 360)

# ----- base array ----------------------
interp1_sst  =  np.zeros((12,458,360))
interp2_sst  =  np.zeros((12,180,360))

# ----  interpolate  --------------------
for i in range(12):
    for j in range(458):
        interp1_sst[i,j,:]  =  np.interp(f1.lon.data,f0.xh.data,f0.tos.data[i,j,:])

for i in range(12):
    for j in range(360):
        interp2_sst[i,:,j]  =  np.interp(f1.lat.data,f0.yh.data,interp1_sst[i,:,j])

# ----  remove the nan value  -----------
from numpy import nan


interp4_sst  =  interp2_sst.copy()
for i in range(12):
    for j in range(360):
        noun_nan  =  interp2_sst[i,:,j][np.logical_not(np.isnan(interp2_sst[i,:,j]))]
        print(noun_nan)
        interp4_sst[i,:,j]  =  np.interp(f1.lat.data,f1.lat.data[np.logical_not(np.isnan(interp2_sst[i,:,j]))],noun_nan)

interp3_sst  =  interp4_sst.copy()
for i in range(12):
    for j in range(180):
        noun_nan = interp4_sst[i, j, :][np.logical_not(np.isnan(interp4_sst[i, j, :]))]
        interp3_sst[i, j, :] = np.interp(f1.lon.data,f1.lon.data[np.logical_not(np.isnan(interp4_sst[i, j, :]))], noun_nan)

f1.SST_cpl.data  =  interp4_sst

import os
os.system('rm -rf /home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c221112.nc')
f1.to_netcdf('/home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c221112.nc')