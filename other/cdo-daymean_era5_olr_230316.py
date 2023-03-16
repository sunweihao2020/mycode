'''
2023-3-16
This script calculate daymean using cdo
'''
import os
import xarray as xr

path0  =  '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float/'
all_file  =  os.listdir(path0)

path_out  =  '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_daymean/'


for ffff in all_file:
    os.system('cdo daymean '+path0+ffff+' '+path_out+ffff)