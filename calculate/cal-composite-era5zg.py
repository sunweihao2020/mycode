'''
2021/2/5
使用era5数据zg数据进行合成
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
import re
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)
year = np.array(list(a.keys()))
day = np.array(list(a.values()))
year = year.astype(int)
day = day.astype(np.int)

path = "/data1/ERA5/datasets/muti-levels/daily/zg/"
file_list0 = os.listdir(path)
file_list = []
for ff in file_list0:
    if "float" in ff:
        file_list.append(ff)
    else:
        continue
file_list.sort()
del file_list0
del file_list[0:12] #现在是从1980年一月开始的了

zg = ma.zeros((61,19,181,360))
#原数据是按月分的，接下来解决数据定位问题，先分到月，再分日期
for yyyy in range(0,2):
    location = day[yyyy]
    #现在来确定一下日期
    if leap_year(year[yyyy]):
        mm = month2
    else:
        mm = month1
    j = 0
    #减去之前月份的总天数，至此定位完成
    for dddd in range(location-30,location+31):
        #开始定位dddd
        mm2 = out_date(year[yyyy],dddd)[6]
        location2 = dddd-np.sum(mm[0:int(mm2)-1])-1 #该文件中第几个时次
        ff = Nio.open_file("/data1/ERA5/datasets/muti-levels/daily/zg/"+"zg."+str(year[yyyy])+"-0"+mm2+"_float.nc")
        z0 = ff.variables["z"][:]
        z1 = z0[location2,::-1,:,:]
        zg[j,:,:,:] += z1/2
        j += 1

#取一下维度
f2 = Nio.open_file("/data1/ERA5/datasets/muti-levels/daily/zg/zg.1991-01_float.nc")
level = f2.variables["level"][::-1]
lat = f2.variables["latitude"][:]
lon = f2.variables["longitude"][:]
a_z = {'longname': 'geopotential','units': 'm**2 s**-2','valid_range': [-1000000000000000.0, 1000000000000000.0]}
time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-era5zg',time,level,lon,lat)
add_variables(fout,'z',zg,a_z,1)


fout.close()





