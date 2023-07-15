'''
2023-5-23
This script calculate the climate average fot the spv
'''
import os
import numpy as np
import xarray as xr

src_path = '/home/sun/wd_disk/merra2_modellev/spv/cdo/'

'''In the following script I calculate three climate spv - daily pentad monthly'''
# ========= 1. climatological daily ==================
f0 = xr.open_dataset(src_path + 'spv_daily_1980_2019.nc')
print(f0)