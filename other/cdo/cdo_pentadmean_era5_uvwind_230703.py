'''
2023-7-3
This script calculate pentad-mean using cdo for slp data
'''
import os

path0 = '/home/sun/temporary/era5_daily_single_layer/'
path1 = '/home/sun/temporary/era5_pentad_single_layer/'

lists = os.listdir(path0) 
list_uv = []
for ff in lists:
    if 'component_of_wind' in ff:
        list_uv.append(ff)

list_uv.sort()
for ffff in list_uv:
    os.system('cdo timselmean,5 ' + path0 + ffff + ' ' + path1 + ffff)