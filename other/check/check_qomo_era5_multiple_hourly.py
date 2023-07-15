'''
2023-6-20
This code check the era5/hourly/multiple data quality
'''
import subprocess
import os

path0 = '/data1/other_data/DataUpdate/ERA5/new-era5/hourly/multiple/'
var_name = ['geopotential', 'omega', 'relatively_humidity', 'temperature', 'uwind', 'vwind']

error_file = []
for vvvv in var_name:
    path1 = path0 + vvvv + '/'
    all_file = os.listdir(path1)
    for ffff in all_file:
        cmd = 'ncdump -h ' + path1 + ffff
        a, b = subprocess.getstatusoutput(cmd) # a获取命令执行状态， b获取命令执行后输出
        if 'Unknown' in b:
            error_file.append(ffff)
        else:
            #print('True')
            continue

with open('/data5/2019swh/error_file.txt', 'w') as f:
    f.writelines(error_file)