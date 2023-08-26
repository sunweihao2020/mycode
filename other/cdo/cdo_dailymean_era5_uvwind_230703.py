'''
2023-7-19
This script calculate daily-mean using cdo for slp data
'''
import os

path0 = '/home/sun/segate2/era5-single-hourly/'
path1 = '/home/sun/temporary/era5_daily_single_layer/'

lists = os.listdir(path0) 
list_uv = []
for ff in lists:
    if 'component_of_wind' in ff:
        list_uv.append(ff)

list_uv.sort()
for ffff in list_uv:
    os.system('cdo daymean ' + path0 + ffff + ' ' + path1 + ffff)