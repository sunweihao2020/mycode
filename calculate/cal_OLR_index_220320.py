'''
This script plot the area-averaged OLR index over the maritime continent
'''
import xarray as xr
import numpy as np
import os

path0 = '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_daymean/'

# divide the maritime continent area
lon1 = 100 ; lon2 = 130 ; lat1 = 10 ; lat2 = -5

def calculate_area_avg():
    f_list = os.listdir(path0) ; f_list.sort()

    # claim the base array
    olr_index = np.zeros((83, 365))

    year = 0
    for ffff in f_list:
        f0 = xr.open_dataset(path0 + ffff).sel(longitude=slice(lon1, lon2), latitude=slice(lat1, lat2))

        for dddd in range(365):
            olr_index[year, dddd] = np.average(f0['ttr'].data[dddd])

        year += 1

    return olr_index

olr_index = calculate_area_avg()

# 4. Write to ncfile
ref_f = xr.open_dataset(path0 + '1941_hourly_OLR.nc')
ncfile  =  xr.Dataset(
                {
                    'ttr_avg': (["year", "time",], olr_index),
                },
                coords={
                    "time": (["time"], np.linspace(1,365,365,dtype=int)),
                    "year": (["year"], np.linspace(1940,2022,83,dtype=int)),
                },
                )
ncfile['ttr_avg'].attrs = ref_f['ttr'].attrs
ncfile.attrs['description'] = 'created on 2023-3-20. This is maritime continent area-averaged OLR based on ERA5 data, area slice is (100-130E, -5-10N)'
ncfile.to_netcdf('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_daily.nc')
