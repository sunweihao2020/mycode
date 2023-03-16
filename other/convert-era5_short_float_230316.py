'''
2023-3-16
Convert era5 single layer from short to float
'''
import os
import xarray as xr

path0  =  '/home/sun/wd_disk/down_ERA5_hourly_OLR/'
all_file  =  os.listdir(path0)

path_out  =  '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float/'


for ffff in all_file:
    f0 = xr.open_dataset(path0 + ffff)
    f1 = f0.drop_vars(['ttr'])
    f1['ttr']  =  (('time', 'latitude', 'longitude'), f0['ttr'].data)
    f1['ttr'].attrs  =  f0['ttr'].attrs
    f1.to_netcdf(path_out + ffff)