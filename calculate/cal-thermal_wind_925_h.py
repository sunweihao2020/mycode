'''
2021/5/31
本代码基于925hPa的位势高度分布来计算热成风
计算方法：比如925-850的厚度、925-700的厚度，即每一层和925hPa的厚度差梯度
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *

f  =  Nio.open_file("/data5/2019swh/data/composite3.nc")
h  =  f.variables["H"][:]

lat =  f.variables["lat"][:]
lon =  f.variables["lon"][:]
lev =  f.variables["level"][:]

h925  =  h[:,3,:,:]
h_a   =  ma.zeros(h[:,4:,:,:].shape)
for ll in range(0,h_a.shape[1]):
    h_a[:,ll,:,:]  =  h[:,ll+4,:,:] - h925

disy,disx,location = cal_xydistance(lat,lon)

sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat

g = 9.8
constant1  =  g/ff
constant1[180]  =  1

#计算温度梯度
h_y  =  np.gradient(h_a,location,axis=2)
h_x  =  ma.zeros(h_y.shape)
for yy in range(0, h_a.shape[2]):
    h_x[:, :, yy, :] = np.gradient(h_a[:,:, yy, :], disx[yy], axis=2)

vt  =  ma.zeros(h_y.shape)
ut  =  ma.zeros(h_y.shape)
for tt in range(0,61):
    for zz in range(0,38):
        for xx in range(0,576):
            vt[tt,zz,:,xx]  =  constant1*h_x[tt,zz,:,xx]
            ut[tt,zz,:,xx]  =  -1*constant1*h_y[tt,zz,:,xx]

time = np.arange(0,61)
a_v = {'longname': 'thermal_wind', 'units': 'm s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
fout = create_nc_multiple('/data5/2019swh/data/', "thermal_wind_925hpa", time, lev[4:], lon, lat)
add_variables(fout, 'thermal_u', ut, a_v, 1)
add_variables(fout, 'thermal_v', vt, a_v, 1)
fout.close()

