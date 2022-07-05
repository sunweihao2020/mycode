'''
2021/3/17
本代码使用erain的daymean资料来计算四月的多年平均
计算变量：u v w
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_writenc import *
from module_sun import *
from attribute import *
#with open("/data5/2019swh/data/onsetdate.json",'r') as load_f:
#    a = json.load(load_f)
path = '/data5/2019swh/data/erain_mean/'

u0 = ma.zeros((37,121,240))
v0 = ma.zeros((37,121,240))
w0 = ma.zeros((37,121,240))

u1 = ma.zeros((39,37,121,240))
v1 = ma.zeros((39,37,121,240))
w1 = ma.zeros((39,37,121,240))

#获取维度信息
f0 = Nio.open_file(path+"/erain-daymean-1992.nc")
lat = f0.variables["lat"][:]
lon = f0.variables["lon"][:]
level = f0.variables["level"][:]


for yyyy in range(1980,2019):
    file = path+"erain-daymean-"+str(yyyy)+".nc"
    f1 = Nio.open_file(file)
    u2 = f1.variables["u"][:]
    v2 = f1.variables["v"][:]
    w2 = f1.variables["w"][:]
    u1[yyyy-1980,:,:,:] = np.average(u2[90:120, :, :, :], axis=0)
    v1[yyyy-1980,:,:,:] = np.average(v2[90:120, :, :, :], axis=0)
    w1[yyyy-1980,:,:,:] = np.average(w2[90:120, :, :, :], axis=0)

u0 = np.average(u1,axis=0)
v0 = np.average(v1,axis=0)
w0 = np.average(w1,axis=0)

time = np.array([1])

fout = create_nc_multiple('/data5/2019swh/data/', 'april-mean-erain', time, level[::-1], lon, lat[::-1])

add_variables(fout, 'w',w0[::-1,::-1,:],a_omega,1)
add_variables(fout, 'u', u0[::-1,::-1,:], a_uwind, 1)
add_variables(fout, 'v', v0[::-1,::-1,:], a_vwind, 1)

fout.close()
