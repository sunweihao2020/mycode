'''2020/11/30
所用资料：OISST
要素 ：计算合成平均的海温
level ：单层
时间跨度： 1982-2016 35年
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
os.system("rm -rf /data5/2019swh/data/composite_OISST.nc")
sys.path.append("/data5/2019swh/mycode/module/")
from module_composite_average import *
from module_writenc import *
from attribute import *

with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

ff = Nio.open_file("/data5/2019swh/data/OISST/1987_279.nc")
lat = ff.variables["lat"][:]
lon = ff.variables["lon"][:]
s1  =   ff.variables["sst"][:]

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
years = year.astype(int)
day = day.astype(np.int)

location = [str(x) for x in day]  #从日期回归文件位置
path='/data5/2019swh/data/OISST/'

sst = ma.zeros((61,720,1440))
for i in range(0,61):
    sst[i,:,:] = ma.array(sst[i,:,:],mask=s1.mask)

year2 = year[2:37]
day2  = day[2:37]
variables=['sst']
end = 35
first = 0

for yyyy in range(0,35):
    day0 = day2[yyyy]
    j = 0
    for dddd in np.arange(day0-30,day0+31):
        f1 = Nio.open_file(path +year2[yyyy]+"_"+str(dddd)+".nc")
        sst_1 = f1.variables["sst"][:]

        sst[j,:,:] += sst_1[:,:]/(end-first)

        j += 1



time = np.arange(0,61)

fout = create_nc_single('/data5/2019swh/data/','composite_OISST',time,lon,lat)
a_t={'longname': 'temperature','units': 'degC','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'SST',sst,a_t,0)

fout.close()
