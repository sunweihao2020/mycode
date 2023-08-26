'''
2023-7-16
This script calculate the correlation between onset dates and LSTC/OLR index
The difference is that it is partial correlation which remove each signal from each other
'''
import numpy as np
import xarray as xr
import sys

sys.path.append("/home/sun/mycode/module/")
from module_sun import *

f0 = xr.open_dataset('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/onset_dates_with_pentad_OLR_LSTC_detrend.nc')

lstc = f0['onset_with_lstc'].data
olr  = f0['onset_with_olr'].data
lstc_olr = f0['lstc_with_olr'].data

partial_lstc = np.zeros(73)
partial_olr  = np.zeros(73)

for tt in range(73):
    partial_lstc[tt] = cal_partial_correlation(lstc[tt], olr[tt], lstc_olr[tt])
    partial_olr[tt]  = cal_partial_correlation(olr[tt],  lstc[tt], lstc_olr[tt])

print(partial_olr)
ncfile  =  xr.Dataset(
                    {
                        'onset_with_lstc_partial': (["time",], partial_lstc),
                        'onset_with_olr_partial': (["time",], partial_olr),
                    },
                    coords={
                        "time": (["time"], np.linspace(1,73,73)),
                    },
                    )
ncfile.attrs['description'] = 'created on 2023-7-16. This file includes the correlation between onset date and OLR/LSTC index. Time resolution is pentad. All the variable has been detrend, the variable in it is partial correlation'

ncfile.to_netcdf('/home/sun/data/ERA5_data_monsoon_onset/index/correlation/partial_correlation_onset_dates_with_pentad_OLR_LSTC_detrend.nc')