'''
2023-7-19
This script make time-series for the pentad 20 to 25, 1940 to 2022 ERA5 wind data
'''
import os
import numpy as np
import xarray as xr

path0 = '/home/sun/temporary/era5_pentad_single_layer/'
file_list = os.listdir(path0)

u_file = []
v_file = []
slp_file = []
for ffff in file_list:
    if '10m_v_component_of_wind' in ffff:
        v_file.append(ffff)
    elif '10m_u_component_of_wind' in ffff:
        u_file.append(ffff)
    elif 'mean_sea_level_pressure' in ffff:
        slp_file.append(ffff)


#print(len(u_file)) ; print(len(v_file))
u_file.sort() ; v_file.sort() ; slp_file.sort()

# Claim the data array
uwind = np.zeros((83, 6, 181, 360))
vwind = uwind.copy()
slp   = uwind.copy()

start_pentad = 19
for i in range(83):
    fu = xr.open_dataset(path0 + u_file[i]).isel(time=slice(19, 25))
    fv = xr.open_dataset(path0 + v_file[i]).isel(time=slice(19, 25))
    fl = xr.open_dataset(path0 + slp_file[i]).isel(time=slice(19, 25))

    uwind[i] = fu['u10'].data
    vwind[i] = fv['v10'].data
    slp[i]   = fl['msl'].data

ncfile  =  xr.Dataset(
{
    "uwind": (["year", "pentad", "lat", "lon"], uwind),
    "vwind": (["year", "pentad", "lat", "lon"], vwind),
    "slp": (["year", "pentad", "lat", "lon"], slp),
},
coords={
    "year": (["year"], np.linspace(1940, 2022, 83)),
    "pentad": (["pentad"], np.linspace(20, 25, 6)),
    "lat":  (["lat"],  fu['latitude'].data),
    "lon":  (["lon"],  fu['longitude'].data),
},
)
ncfile['uwind'].attrs['description']  =  'uwind from 1940 to 2022 for the period 20 to 25 pentads'
ncfile['vwind'].attrs['description']  =  'vwind from 1940 to 2022 for the period 20 to 25 pentads'
ncfile.attrs['description'] = 'Created on 2023-7-20. This file is for the regression calculation, including pentad 20to25 pentad and for the year 1940 to 2022'
ncfile.to_netcdf("/home/sun/data/long_time_series_after_process/ERA5_10mwind_slp_pentad20to25_1940_2022.nc")