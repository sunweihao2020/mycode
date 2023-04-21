'''
2023-3-4
This script calculate the correlation between the onset day and differenct indexs
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd
import math

index_file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/ERA5_single_monthly_OLR_1940_2022.nc').sel(year=slice(1959, 2021))
onset_file = xr.open_dataset('/home/sun/data/onset_day_data/ERA5_onset_day_include_early_late_years.nc')

# Onset day series
onset_dates = onset_file['onset_day'].data

# Prepare the indexs
olr = index_file['monthly_olr'].data

print(olr)



# ============== Now all the index is OK ==========================

# Calculate the correlation
# 2.1 Same year correlation
correlation_olr = np.zeros((12, 181, 360))


for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
                corre_index_u   = stats.pearsonr(onset_dates - np.average(onset_dates), olr[:, tttt, latt, lonn] - np.average(olr[:, tttt, latt, lonn])) # First value is statistic
                correlation_olr[tttt, latt, lonn]   = corre_index_u[0]

#print(correlation_sp)
# 3. Save the correlation to the array
ncfile  =  xr.Dataset(
                    {
                        'onset_with_olr': (["time", "lat", "lon"], correlation_olr),
                    },
                    coords={
                        "lat": (["lat"], index_file.lat.data),
                        "lon": (["lon"], index_file.lon.data),
                        "time": (["time"], np.linspace(1,12,12)),
                    },
                    )
ncfile.attrs['description'] = 'created on 2023-3-16. This file includes the correlation between onset date and OLR'

ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/onset_dates_with_OLR.nc')
#print(correlation_sst)