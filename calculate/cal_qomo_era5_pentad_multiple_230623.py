'''
2023-6-23
This code calculate pentad average era5 daily multiple data
'''
import os

path0 = '/data1/other_data/DataUpdate/ERA5/new-era5/pentad/multiple/'
path1 = '/data1/other_data/DataUpdate/ERA5/new-era5/daily/multiple/'
test_path = '/data1/other_data/DataUpdate/ERA5/new-era5/other/'
var_name = ['geopotential', 'omega', 'relatively_humidity', 'temperature', 'uwind', 'vwind']


for vvvv in var_name:
    path3 = path1 + vvvv + '/'
    for yyyy in range(1940, 2023):
        os.system('cdo -b F64 cat ' + path3 + '*_'+str(yyyy)+'* ' + test_path + str(yyyy) + vvvv + '.nc')
    os.system('mkdir -p ' + path0 + vvvv)
    end_path = path0 + vvvv + '/'
    for yyyy in range(1940, 2023):
        os.system('cdo timselmean,5 ' + test_path + str(yyyy) + vvvv + '.nc ' + end_path + 'ERA5_multiple_pentad_' + str(yyyy) + '.nc')
