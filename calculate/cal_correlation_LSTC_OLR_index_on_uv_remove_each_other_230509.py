'''
2023-05-09
This script calculate the correlation between LSTC/OLR and u/v
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd
from sklearn.linear_model import LinearRegression

day_jul = 180; day_jun = 150; day_may = 120 ; day_apr = 90 ; day_march = 60 ; day_feb = 31; day_jan = 0
day_list = [day_jan, day_feb, day_march, day_apr, day_may, day_jun, day_jul]

def calculate_monthly_mean(var):
    '''This dunction calculate the monthly mean variables from Feb to Jun (4)'''
    # 1. Claim the monthly avg array
    mon_avg = np.zeros((63, 6))

    for yyyy in range(63):
        for i in range(6):
            mon_avg[yyyy, i] = np.average(var[yyyy, day_list[i] : day_list[i+1]])
    
    return mon_avg


# ============ Read index file =======================
f1 = xr.open_dataset('/home/sun/data/other_data/maritime_avg_OLR/OLR_maritime_area_average_monthly.nc').sel(year=slice(1959, 2021))

# f2 need to calculate monthly average
f2 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc')
ls_diff  = calculate_monthly_mean(f2['ls_diff'].data)

#rint(f1) # Shape (63, 12)
#rint(ls_diff.shape) # Shape (63, 6), here only six month from 1-6

# ============ Remove signals from each other =======
lineModel = LinearRegression()
lineModel.fit(np.array(ls_diff[:, 3]).reshape((len(ls_diff[:, 3]), 1)), np.array(f1['ttr_avg_mon'][:, 3]).reshape((len(f1['ttr_avg_mon'][:, 3])), 1)) #x, y
a1 = lineModel.coef_[0][0]
b  = lineModel.intercept_[0]
olr_remove_lstc = f1['ttr_avg_mon'][:, 3] - (a1*ls_diff[:, 3] + b)

lineModel.fit(np.array(f1['ttr_avg_mon'][:, 3]).reshape((len(f1['ttr_avg_mon'][:, 3]), 1)), np.array(ls_diff[:, 3]).reshape((len(ls_diff[:, 3])), 1)) #x, y
a1 = lineModel.coef_[0][0]
b  = lineModel.intercept_[0]
lstc_remove_olr = ls_diff[:, 3] - (a1*f1['ttr_avg_mon'][:, 3] + b)

# ============ Read circulation file ==================
f3 = xr.open_dataset("/home/sun/data/ERA5_data_monsoon_onset/index/ERA5_single_monthly_1959_2021.nc").sel(month=4)

# ============ Claim correlation matrix ===============
correlation_u_LSTC = np.zeros((181, 360)); correlation_v_LSTC = np.zeros((181, 360)); correlation_u_OLR = np.zeros((181, 360)); correlation_v_OLR = np.zeros((181, 360))

# ============ Calculate correlation ==================
for i in range(181):
    for j in range(360):
        #print(ls_diff[:, 3] - np.average(ls_diff[:, 3]))
        #print(f3['monthly_u'][:, i, j] - np.average(f3['monthly_u'][:, i, j]))
        correlation_u_LSTC[i, j] = stats.pearsonr(lstc_remove_olr - np.average(lstc_remove_olr), f3['monthly_u'][:, i, j] - np.average(f3['monthly_u'][:, i, j]))[0]
        correlation_v_LSTC[i, j] = stats.pearsonr(lstc_remove_olr - np.average(lstc_remove_olr), f3['monthly_v'][:, i, j] - np.average(f3['monthly_v'][:, i, j]))[0]
        correlation_u_OLR[i, j]  = stats.pearsonr(olr_remove_lstc - np.average(olr_remove_lstc), f3['monthly_u'][:, i, j] - np.average(f3['monthly_u'][:, i, j]))[0]
        correlation_v_OLR[i, j]  = stats.pearsonr(olr_remove_lstc - np.average(olr_remove_lstc), f3['monthly_v'][:, i, j] - np.average(f3['monthly_v'][:, i, j]))[0]

ncfile  =  xr.Dataset(
{
    "correlation_u_LSTC": (["lat", "lon"], correlation_u_LSTC),
    "correlation_v_LSTC": (["lat", "lon"], correlation_v_LSTC),
    "correlation_u_OLR": (["lat", "lon"],  correlation_u_OLR),
    "correlation_v_OLR": (["lat", "lon"],  correlation_v_OLR),
},
coords={
    "lat": (["lat"], f3.lat.data),
    "lon": (["lon"], f3.lon.data),
},
)
ncfile.attrs['description']  =  'This file includes correlation between LSTC/OLR index and global uv field (10m wind) using ERA5 data. The signals has been removed from each other.'
ncfile.attrs['script']  =  'cal_correlation_LSTC_OLR_index_on_uv_remove_each_other_230509.py'
ncfile.to_netcdf("/home/sun/data/ERA5_data_monsoon_onset/correlation/correlation_LSTC_OLR_10wind_remove_each_other.nc")
