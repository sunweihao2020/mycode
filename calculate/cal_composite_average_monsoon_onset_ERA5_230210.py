'''
2023-02-10
This script calculate the composite average before and after monsoon onset using ERA5 data
The early and late onset year composite is also calculated
'''
import xarray as xr
import numpy as np

# ------------ 1. Read the onset date data --------------------
date_file  =  xr.open_dataset('/home/sun/data/onset_day_data/ERA5_onset_day_include_early_late_years.nc')
print(date_file)