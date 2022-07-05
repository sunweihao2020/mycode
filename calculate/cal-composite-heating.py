'''
2021/1/23
使用资料：日平均的加热资料
资料路径：/data5/2019swh/merra2/tdt
合成分析到季风爆发
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

years = np.array(list(a.keys()))
days = np.array(list(a.values()))
years = years.astype(np.int)
days = days.astype(np.int)

days -= 1 #定位文件位置

#取维度信息
f = Nio.open_file(path0+"MERRA2_100.tavg3_3d_tdt_Np.19800121.SUB.nc")
level = f.variables["lev"][:]
lat = f.variables["lat"][:]
lon = f.variables["lon"][:]

#初始化
tdt0 = ma.zeros((61,25,144,288))

#取第一年的数据
y0 = 1980
path0 = '/data5/2019swh/merra2/tdt/1980/'
file0 = os.listdir(path0)
file0.sort()
j0 = 0
for i in range(days[0]-30,days[0]+31):
    f0 = Nio.open_file(path0+file0[i])
    tdt0[j0,:,:,:] =