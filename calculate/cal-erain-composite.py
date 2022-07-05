'''
2021/3/15
本代码使用前面计算日平均的erain资料
计算合成分析后的结果
时间跨度1980-2018
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
from module_sun import *
from attribute import *
path0 = '/data5/2019swh/data/erain_mean/'
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

year = np.array(list(a.keys()))
day = np.array(list(a.values()))
year = year.astype(int)
day = day.astype(np.int)
day -= 1
time = np.arange(0,61)+1
var = ['t','w','vo','d','u','v','rh']
#获取维度信息
f0 = Nio.open_file(path0+"/erain-daymean-1992.nc")
lat = f0.variables["lat"][:]
lon = f0.variables["lon"][:]
level = f0.variables["level"][:]

cmd0 = 'var0 = ma.zeros((61,37,121,240))'
for vvvv in var:
    exec(cmd0.replace('var',vvvv))
start = 0
end = 39
for yyyy in range(start,end):
    f1 = Nio.open_file(path0+"erain-daymean-"+str(year[yyyy])+".nc")
    cmd1 = 'mm1 = f1.variables["mm"][:]'
    for vvvv in var:
        exec(cmd1.replace('mm',vvvv))
    location = day[yyyy]
    j = 0
    for dddd in range(location-30,location+31):
        cmd3 = 'xx0[j,:,:,:] += xx1[dddd,:,:,:]/(end-start)'
        for vvvv in var:
            exec(cmd3.replace('xx',vvvv))
        j+=1

time = np.arange(0, u0.shape[0])
fout = create_nc_multiple('/data5/2019swh/data/', 'composite-erain', time, level[::-1], lon, lat[::-1])
add_variables(fout, 't', t0[:,::-1,::-1,:], a_T, 1)
add_variables(fout, 'w',w0[:,::-1,::-1,:],a_omega,1)
a_vo = {'longname': 'vorticity', 'units': 's-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout, 'vo', vo0[:,::-1,::-1,:], a_vo, 1)
add_variables(fout, 'd', d0[:,::-1,::-1,:], a_vo, 1)
add_variables(fout, 'u', u0[:,::-1,::-1,:], a_uwind, 1)
add_variables(fout, 'v', v0[:,::-1,::-1,:], a_vwind, 1)
a_rh = {'longname': 'relative humidity', 'units': '1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout, 'rh', rh0[:,::-1,::-1,:], a_rh, 1)
fout.close()