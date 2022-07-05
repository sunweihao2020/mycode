'''
2020/11/18
计算降水的合成平均
使用资料：GPCP(1997-2019)
单层（总降水）
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
sys.path.append("/data5/2019swh/mycode/module/")
from module_writenc import *
from attribute import a_pre
path0 = '/data5/2019swh/mydown/GPCP/'
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
year = year.astype(int)
year   = year[17:]
day    = day[17:]
day = day.astype(np.int)
day -= 1
time = np.arange(0,61)+1
level = np.array([1000])
#测试数据获取维度
pp = "/data5/2019swh/mydown/GPCP/2006/gpcp_v01r03_daily_d20060821_c20170530.nc"
f = Nio.open_file(pp)
lat = f.variables["latitude"][:]
lon = f.variables["longitude"][:]
#pre = f.variables["precip"][0,:,:]
#计算合成平均
precp = ma.zeros((61,180,360))
years = np.arange(1997,2020)
end = 20
start = 0
for yyyy in range(start,end):
    path = path0+str(years[yyyy])+"/"
    files = os.listdir(path)
    files.sort()
    day0 = day[yyyy]
    j = 0
    for dddd in np.arange(day0 - 30, day0 + 31):
        ff = Nio.open_file(path + files[dddd])
        precp1 = ff.variables["precip"][:]
        precp[j, :, :] += precp1[0, :, :] / (end - start)
        j += 1




fout = create_nc_single('/data5/2019swh/data/','composite_GPCP',time,lon,lat)
add_variables(fout,'precipitation',precp,a_pre,0)

fout.close()
