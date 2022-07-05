'''2020/11/30
所用资料：era-interim
要素 ：计算合成平均的10m风
level ：单层
时间跨度： 1980-2018 39年
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
os.system("rm -rf /data5/2019swh/data/composite_erain_10u.nc")
sys.path.append("/data5/2019swh/mycode/module/")
from module_composite_average import *
from module_writenc import *
from attribute import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

ff = Nio.open_file("/data5/2019swh/data/erain/wind/V10m.2014.18.nc")
lat = ff.variables["latitude"][:]
lon = ff.variables["longitude"][:]

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)
day -= 1
location = [str(x) for x in day]  #从日期回归文件位置
path='/data5/2019swh/data/erain/wind/'

u10 = np.zeros((61,181,360))
v10 = np.zeros((61,181,360))

variables=['u10','v10']
end = 39
first = 0

for yyyy in range(0,39):
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+31):
        f1 = Nio.open_file(path + "u10_"+year[yyyy]+"_.nc")
        f2 = Nio.open_file(path + "v10_" + year[yyyy] + "_.nc")
        u10_1 = f1.variables["u10"][:]
        v10_1 = f2.variables["v10"][:]
        u10[j,:,:] += u10_1[dddd,:,:]/(end-first)
        v10[j, :, :] += v10_1[dddd, :, :] / (end - first)
        j += 1

u = u10[:,::-1,:]
v = v10[:,::-1,:]

time = np.arange(0,61)
lev  = np.array([1000])
fout = create_nc_single('/data5/2019swh/data/','composite_u10v10',time,lon,lat[::-1])
add_variables(fout,'u10m',u,a_uwind,0)
add_variables(fout,'v10m',v,a_vwind,0)
fout.close()
