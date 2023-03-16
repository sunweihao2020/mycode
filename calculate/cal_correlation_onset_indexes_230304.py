'''
2023-3-4
This script calculate the correlation between the onset day and differenct indexs
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd
import math

index_file = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/ERA5_single_monthly_1959_2021.nc')
onset_file = xr.open_dataset('/home/sun/data/onset_day_data/ERA5_onset_day_include_early_late_years.nc')

# Onset day series
onset_dates = onset_file['onset_day'].data

# Prepare the indexs
sst        = index_file['monthly_sst'].data
zonal_wind = index_file['monthly_u'].data
meri_wind  = index_file['monthly_v'].data
sp         = index_file['monthly_sp'].data

sp_sub_land = sp.copy()

# Calculate the Land-Sea difference, Here I calculate through subtracting sp over the Indian Peninsula from the sp over sea
# 1. Calculate the area-average value over the Indian Peninsula
mask_file = xr.open_dataset('/home/sun/data/mask/ERA5_land_sea_mask_1x1.nc')

# Range for Indian Peninsula
lat_range = slice(20, 5)
lon_range = slice(70, 90)

sp_land   = index_file.sel(lat=lat_range, lon=lon_range)['monthly_sp'].data
mask_land = mask_file.sel(latitude=lat_range, longitude=lon_range)['lsm'].data[0]

for i in range(63):
    for j in range(12):
        sp_land_mask = sp_land[i, j].copy()
        sp_land_mask[mask_land < 0.5] = np.nan
        sp_ocean_mask = sp[i, j].copy()
        sp_ocean_mask[mask_file['lsm'].data[0] > 0.1] = np.nan
        sp_sub_land[i, j] = sp_ocean_mask - np.nanmean(sp_land_mask)



# ============== Now all the index is OK ==========================

# Calculate the correlation
# 2.1 Same year correlation
correlation_sst = np.zeros((12, 181, 360))
correlation_u   = correlation_sst.copy()
correlation_v   = correlation_sst.copy()
correlation_sp  = correlation_sst.copy()

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
            # Skip the NAN for sst
            if np.isnan(sst[:, tttt, latt, lonn]).any():
                continue
            else:
                corre_index_sst = stats.pearsonr(onset_dates - np.average(onset_dates), sst[:, tttt, latt, lonn] - np.average(sst[:, tttt, latt, lonn])) # First value is statistic
                correlation_sst[tttt, latt, lonn] = corre_index_sst[0]

#print(correlation_sst)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
                corre_index_u   = stats.pearsonr(onset_dates - np.average(onset_dates), zonal_wind[:, tttt, latt, lonn] - np.average(zonal_wind[:, tttt, latt, lonn])) # First value is statistic
                correlation_u[tttt, latt, lonn]   = corre_index_u[0]

#print(correlation_u)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
                corre_index_v   = stats.pearsonr(onset_dates - np.average(onset_dates), meri_wind[:, tttt, latt, lonn] - np.average(meri_wind[:, tttt, latt, lonn])) # First value is statistic
                correlation_v[tttt, latt, lonn]   = corre_index_v[0]

#print(correlation_v)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
            # Skip the NAN for sst
            if np.isnan(sp_sub_land[:, tttt, latt, lonn]).any():
                continue
            else:
                corre_index_sp = stats.pearsonr(onset_dates - np.average(onset_dates), sp_sub_land[:, tttt, latt, lonn] - np.average(sp_sub_land[:, tttt, latt, lonn])) # First value is statistic
                correlation_sp[tttt, latt, lonn]  = corre_index_sp[0]

#print(correlation_sp)

                

# 2.2 Previous year correlation
correlation_sst_previous = np.zeros((12, 181, 360))
correlation_u_previous   = correlation_sst_previous.copy()
correlation_v_previous   = correlation_sst_previous.copy()
correlation_sp_previous  = correlation_sst_previous.copy()

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
            # Skip the NAN for sst
            if np.isnan(sst[:, tttt, latt, lonn]).any():
                continue
            else:
                corre_index_sst = stats.pearsonr(onset_dates[1:] - np.average(onset_dates[1:]), sst[:-1, tttt, latt, lonn] - np.average(sst[:-1, tttt, latt, lonn])) # First value is statistic
                correlation_sst_previous[tttt, latt, lonn] = corre_index_sst[0]

#print(correlation_sst)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
                corre_index_u   = stats.pearsonr(onset_dates[1:] - np.average(onset_dates[1:]), zonal_wind[:-1, tttt, latt, lonn] - np.average(zonal_wind[:-1, tttt, latt, lonn])) # First value is statistic
                correlation_u_previous[tttt, latt, lonn]   = corre_index_u[0]

#print(correlation_u)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
                corre_index_v   = stats.pearsonr(onset_dates[1:] - np.average(onset_dates[1:]), meri_wind[:-1, tttt, latt, lonn] - np.average(meri_wind[:-1, tttt, latt, lonn])) # First value is statistic
                correlation_v_previous[tttt, latt, lonn]   = corre_index_v[0]

#print(correlation_v)

for tttt in range(12):
    for latt in range(181):
        for lonn in range(360):
            # Skip the NAN for sst
            if np.isnan(sp_sub_land[:, tttt, latt, lonn]).any():
                continue
            else:
                corre_index_sp = stats.pearsonr(onset_dates[1:] - np.average(onset_dates[1:]), sp_sub_land[:-1, tttt, latt, lonn] - np.average(sp_sub_land[:-1, tttt, latt, lonn])) # First value is statistic
                correlation_sp_previous[tttt, latt, lonn]  = corre_index_sp[0]

#print(correlation_sp)
# 3. Save the correlation to the array
ncfile  =  xr.Dataset(
                    {
                        'onset_with_sst': (["time", "lat", "lon"], correlation_sst),
                        'onset_with_sst_previous': (["time", "lat", "lon"], correlation_sst_previous),
                        'onset_with_u': (["time", "lat", "lon"], correlation_u),
                        'onset_with_u_previous': (["time", "lat", "lon"], correlation_u_previous),
                        'onset_with_v': (["time", "lat", "lon"], correlation_v),
                        'onset_with_v_previous': (["time", "lat", "lon"], correlation_v_previous),
                        'onset_with_sp': (["time", "lat", "lon"], correlation_sp),
                        'onset_with_sp_previous': (["time", "lat", "lon"], correlation_sp_previous),
                    },
                    coords={
                        "lat": (["lat"], index_file.lat.data),
                        "lon": (["lon"], index_file.lon.data),
                        "time": (["time"], np.linspace(1,12,12)),
                    },
                    )
ncfile.attrs['description'] = 'created on 2023-3-6. This file includes the correlation between onset date and other variables for the same year and previous year'

ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/many_index_corr_with_onset_dates.nc')
#print(correlation_sst)