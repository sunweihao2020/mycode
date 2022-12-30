'''
2022-12-16
This code interpolate the model output SST to the inputfile SST
In this script i would try to change the time resolution to the daily
Metion: I also need to modify the ice data
'''
input_file  =  '/home/sun/data/model_data/input/daily_sst_model/daily_sst_trans_longitude.nc'
model_sst   =  '/home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c180511.nc'

import xarray as xr
import numpy as np
import scipy

f0  =  xr.open_dataset(input_file)
f1  =  xr.open_dataset(model_sst)

# ----- read lat/lon information --------
print(f0.tos.data.shape)      # (365, 458, 540)
print(f1.SST_cpl.data.shape)  # (12, 180, 360)

'''---------- 1. Deal with the sst data, only need to interpolate to the model sst lon/lat-------------------'''
# ----- base array ----------------------
interp1_sst  =  np.zeros((365,458,360))
interp2_sst  =  np.zeros((365,180,360))

# ----  interpolate  --------------------
for i in range(365):
    for j in range(458):
        interp1_sst[i,j,:]  =  np.interp(f1.lon.data,f0.xh.data,f0.tos.data[i,j,:])

for i in range(365):
    for j in range(360):
        interp2_sst[i,:,j]  =  np.interp(f1.lat.data,f0.yh.data,interp1_sst[i,:,j])

# ----  remove the nan value  -----------
from numpy import nan


interp4_sst  =  interp2_sst.copy()
for i in range(365):
    for j in range(360):
        noun_nan  =  interp2_sst[i,:,j][np.logical_not(np.isnan(interp2_sst[i,:,j]))]
        #print(noun_nan)
        interp4_sst[i,:,j]  =  np.interp(f1.lat.data,f1.lat.data[np.logical_not(np.isnan(interp2_sst[i,:,j]))],noun_nan)

interp3_sst  =  interp4_sst.copy()
for i in range(365):
    for j in range(180):
        noun_nan = interp4_sst[i, j, :][np.logical_not(np.isnan(interp4_sst[i, j, :]))]
        interp3_sst[i, j, :] = np.interp(f1.lon.data,f1.lon.data[np.logical_not(np.isnan(interp4_sst[i, j, :]))], noun_nan)

''' -----------2. Deal with ice data, Here I intepolate monthly ice data to the daily--------------'''
model_ice  =  np.float64(f1['ice_cov'].data)

# To avoid possible problem, I use the average of the Jan and Dec to be the 1st and 365th day for calculate
avg_ice    =  (model_ice[0] + model_ice[11]) / 2

daily_ice_input  =  np.zeros((14,180,360), dtype=np.float32)
daily_ice_input[0] = avg_ice ; daily_ice_input[13] = avg_ice
daily_ice_input[1:13]  =  model_ice

daily_ice_output =  np.zeros((365, 180, 360), dtype=np.float64)
axis_in          =  f1.time.data
axis_out         =  np.linspace(0,364,364,dtype=np.float64)

#for i in range(180):
#    for j in range(360):
#        print(type(model_ice[10, i, j]))
#        daily_ice_output[:,i,j]  =  np.interp(axis_out, axis_in, model_ice[:, i, j])
from scipy import interpolate
month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])
for i in range(180):
    for j in range(360):
        daily_ice_output[0:31, i, j]  =  model_ice[0, i, j]
        daily_ice_output[31:59, i, j]  =  model_ice[1, i, j]
        daily_ice_output[59:90, i, j]  =  model_ice[2, i, j]
        daily_ice_output[90:120, i, j]  =  model_ice[3, i, j]
        daily_ice_output[120:151, i, j]  =  model_ice[4, i, j]
        daily_ice_output[151:181, i, j]  =  model_ice[5, i, j]
        daily_ice_output[181:212, i, j]  =  model_ice[6, i, j]
        daily_ice_output[212:243, i, j]  =  model_ice[7, i, j]
        daily_ice_output[243:273, i, j]  =  model_ice[8, i, j]
        daily_ice_output[273:304, i, j]  =  model_ice[9, i, j]
        daily_ice_output[304:334, i, j]  =  model_ice[10, i, j]
        daily_ice_output[334:365, i, j]  =  model_ice[11, i, j]

import os

'''-------------3. add to dataset-------------------------------------------------------'''
# Metion: Here I delete the preddidle vars to see whether it can be used by model
# The variables included in the file:
# 1. date YYYYMMDD for example first value is 116: Jan 16th
# 2. datesec 43200 and 0 appear alternately, 43200 corresponds to hour 12 I think is noon
# 3. time Metion that its meaning is since 01-01, thus first value is 15.5 and date is 16
#
# Here I map the first value to the 01-01: first value of date is 101
#                                          datesec I set all to the 0
#                                          first value of time is 0

''' 1. make new date'''
month_day  =  np.array([31,28,31,30,31,30,31,31,30,31,30,31])
date_new   =  np.array([], dtype=int)

j = 1 # The month number
for mmmm in month_day:
    origin_date  =  j * 100
    for dddd in range(mmmm):
        date_new = np.append(date_new, origin_date + 1 + dddd)

    j += 1

''' 2. make new datesec'''
datesec_new    =  np.zeros((365), dtype=int)

''' 3. make new time'''
time_new       =  np.linspace(0,364,364, dtype=np.float64)

''' ----------- create New input SST -------------'''
ncfile  =  xr.Dataset(
    {
        "date": (["time"], date_new),
        "datesec": (["time"], datesec_new),
        "ice_cov": (["time", "lat", "lon"], daily_ice_output),
        "SST_cpl": (["time", "lat", "lon"], interp3_sst),
        #"lat": (["lat"], f1.lat.data),
        #"lon": (["lon"], f1.lon.data),
        #"time": (["time"], np.linspace(0,364,365,dtype=np.float64)),
    },
    coords={
        "lat": (["lat"], f1.lat.data),
        "lon": (["lon"], f1.lon.data),
        "time": (["time"], np.linspace(0, 364, 365, dtype=np.float64)),
    },
    )

ncfile["date"].attrs    =  f1["date"].attrs
ncfile["datesec"].attrs =  f1["datesec"].attrs
ncfile["lon"].attrs     =  f1["lon"].attrs
ncfile["lat"].attrs     =  f1["lat"].attrs
ncfile["ice_cov"].attrs =  f1["ice_cov"].attrs
ncfile["SST_cpl"].attrs =  f1["SST_cpl"].attrs

ncfile["time"].attrs['units']    =  "days since 0000-01-01 00:00:00"
ncfile["time"].attrs['calendar'] =  "365_day"

ncfile.attrs['description']  =  'Generated in 2022-12-19. This file based on the daily sst to drive AGCM model.'
#os.system('rm -rf /home/sun/data/model_data/input/sst_HadOIBl_bc_1x1_2000climo_c221112.nc')
ncfile.to_netcdf('/home/sun/data/model_data/input/daily_sst_model/cam_SST_daily_input.nc', unlimited_dims="time")