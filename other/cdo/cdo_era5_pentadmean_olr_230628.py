'''
2023-6-28
This script cdo daymean the ERA5 OLR hourly data
'''
path0 = '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_daymean/'
path1 = '/home/sun/data/other_data/down_ERA5_hourly_OLR_convert_float_pentadmean/'

import os

file_list = os.listdir(path0)
for ffff in file_list:
    os.system('cdo timselmean,5 '+path0+ffff+' '+path1+ffff)