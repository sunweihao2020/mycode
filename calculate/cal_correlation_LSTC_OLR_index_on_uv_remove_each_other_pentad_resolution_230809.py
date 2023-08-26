'''
2023-08-09
This script calculate the correlation between LSTC/OLR and u/v, the former script is for April mean
This calculate pentad 20-25 during the years 1940 - 2022
'''
import numpy as np
import xarray as xr
from scipy import stats
import pandas as pd
from sklearn.linear_model import LinearRegression


# ============ Read index file =======================
f1 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/regression/regression_uv_to_OLR_to_LSTC_remove_each_other.nc')
#print(f1)

## f2 need to calculate monthly average
#f2 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/quantity_index_monsoon_onset_ERA5.nc')
#ls_diff  = calculate_monthly_mean(f2['ls_diff'].data)
#
##rint(f1) # Shape (63, 12)
##rint(ls_diff.shape) # Shape (63, 6), here only six month from 1-6
#
## ============ Remove signals from each other =======
#lineModel = LinearRegression()
#lineModel.fit(np.array(ls_diff[:, 3]).reshape((len(ls_diff[:, 3]), 1)), np.array(f1['ttr_avg_mon'][:, 3]).reshape((len(f1['ttr_avg_mon'][:, 3])), 1)) #x, y
#a1 = lineModel.coef_[0][0]
#b  = lineModel.intercept_[0]
#olr_remove_lstc = f1['ttr_avg_mon'][:, 3] - (a1*ls_diff[:, 3] + b)
#
#lineModel.fit(np.array(f1['ttr_avg_mon'][:, 3]).reshape((len(f1['ttr_avg_mon'][:, 3]), 1)), np.array(ls_diff[:, 3]).reshape((len(ls_diff[:, 3])), 1)) #x, y
#a1 = lineModel.coef_[0][0]
#b  = lineModel.intercept_[0]
#lstc_remove_olr = ls_diff[:, 3] - (a1*f1['ttr_avg_mon'][:, 3] + b)
#
## ============ Read circulation file ==================
#f3 = xr.open_dataset("/home/sun/data/ERA5_data_monsoon_onset/index/ERA5_single_monthly_1959_2021.nc").sel(month=4)
#
## ============ Claim correlation matrix ===============
correlation_u_LSTC = np.zeros((6, 181, 360)); correlation_v_LSTC = np.zeros((6, 181, 360)); correlation_u_OLR = np.zeros((6, 181, 360)); correlation_v_OLR = np.zeros((6, 181, 360))
#
## ============ Calculate correlation ==================
for t in range(6):
    for i in range(181):
        for j in range(360):
            #print(len(f1['lstc_remove_olr'].data[t] - np.average(f1['lstc_remove_olr'].data[t])))
            correlation_u_LSTC[t, i, j] = stats.pearsonr(f1['lstc_remove_olr'].data[:, t] - np.average(f1['lstc_remove_olr'].data[:, t]), f1['u_detrend'][:, t, i, j] - np.average(f1['u_detrend'][:, t, i, j]))[0]
            correlation_v_LSTC[t, i, j] = stats.pearsonr(f1['lstc_remove_olr'].data[:, t] - np.average(f1['lstc_remove_olr'].data[:, t]), f1['v_detrend'][:, t, i, j] - np.average(f1['v_detrend'][:, t, i, j]))[0]
            correlation_u_OLR[t, i, j]  = stats.pearsonr(f1['olr_remove_lstc'].data[:, t] - np.average(f1['olr_remove_lstc'].data[:, t]), f1['u_detrend'][:, t, i, j] - np.average(f1['u_detrend'][:, t, i, j]))[0]
            correlation_v_OLR[t, i, j]  = stats.pearsonr(f1['olr_remove_lstc'].data[:, t] - np.average(f1['olr_remove_lstc'].data[:, t]), f1['v_detrend'][:, t, i, j] - np.average(f1['v_detrend'][:, t, i, j]))[0]
            

ncfile  =  xr.Dataset(
{
    "correlation_u_LSTC": (["pentad", "lat", "lon"], correlation_u_LSTC),
    "correlation_v_LSTC": (["pentad", "lat", "lon"], correlation_v_LSTC),
    "correlation_u_OLR": (["pentad", "lat", "lon"],  correlation_u_OLR),
    "correlation_v_OLR": (["pentad", "lat", "lon"],  correlation_v_OLR),
},
coords={
    "lat": (["lat"], f1.lat.data),
    "lon": (["lon"], f1.lon.data),
    "pentad": (["pentad"], f1.pentad.data)
},
)
ncfile.attrs['description']  =  'This file includes correlation between LSTC/OLR index and global uv field (10m wind) using ERA5 data. The signals has been removed from each other. It is pentad correlation.'
ncfile.attrs['script']  =  'cal_correlation_LSTC_OLR_index_on_uv_remove_each_other_pentad_resolution_230809.py'
ncfile.to_netcdf("/home/sun/data/ERA5_data_monsoon_onset/correlation/correlation_LSTC_OLR_10wind_pentad_remove_each_other.nc")
