'''
2021/5/24
本代码使用模式层资料来计算热成风
主要是测试一下。。
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *
with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
    a = json.load(load_f)

f = Nio.open_file("/data5/2019swh/mydown/merra_modellev/MERRA2_100.tavg3_3d_asm_Nv.19830617.SUB.nc")

lon = f.variables["lon"][:]
lat = f.variables["lat"][:]
h1  = f.variables["H"][:]
h   = f.variables["H"]
p   = f.variables["PL"][:]

#这里选取72-40层
sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat

#切片
lon2 = lon[48:]
lat2 = lat[110:]

#先把ln的整出来
t    = f.variables["T"][:,:,110:151,48:]

av = np.average(t,axis=0)