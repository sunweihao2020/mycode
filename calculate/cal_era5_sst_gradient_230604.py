'''
2023-6-4
This script calculate the gradient of the sea surface temperature for ERA5 data
'''
import xarray as xr
import numpy as np
import os
import sys
from geopy.distance import distance

path0 = '/home/sun/wd_disk/era5_sst/'
path1 = '/home/sun/wd_disk/era5_sst_gradient/'
f0    = xr.open_dataset(path0 + 'era5_single_sea_surface_temperature_197710_.nc')

# Get the geometry distance information
def cal_xydistance(lat,lon):
    disy = np.array([])
    disx = np.array([])
    for i in range(0, (lat.shape[0]-1)):
        disy = np.append(disy, distance((lat[i], 0), (lat[i + 1], 0)).m)

    for i in range(0, lat.shape[0]):
        disx = np.append(disx, distance((lat[i], lon[0]), (lat[i], lon[1])).m)

    location = np.array([0])
    for dddd in range(0, (lat.shape[0]-1)):
        location = np.append(location, np.sum(disy[:dddd + 1]))

    return disy,disx,location
    
disy,disx,location = cal_xydistance(f0.latitude,f0.longitude)
#print(location)
#print()
filelist = os.listdir(path0)

for ffff in filelist:
    f1 = xr.open_dataset(path0 + ffff)

    sst_gradient = np.gradient(f1['sst'].data,location,axis=1)

    # ----------- save to the ncfile ------------------
    ncfile  =  xr.Dataset(
    {
        "sst_gradient": (["time", "latitude", "longitude"], -1 * sst_gradient),
    },
    coords={
        "time": (["time"], f1.time.data),
        "latitude": (["latitude"], f1.latitude.data),
        "longitude":  (["longitude"],  f1.longitude.data),
    },
    )
    ncfile.attrs['description']  =  'It is the sst gradient from the era5 daily sst file. script is cal_era5_sst_gradient_230604.py'
    ncfile.to_netcdf(path1 + ffff[:-3] + 'gradient' + '.nc')