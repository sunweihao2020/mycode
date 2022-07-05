'''
2021/5/30
本代码基于925hPa的温度分布来计算热成风
计算方法：比如925-850的热成风、925-700的热成风，即每一层和925hPa的平均温度梯度
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
t  =  f.variables["T"][:]

lat =  f.variables["lat"][:]
lon =  f.variables["lon"][:]
lev =  f.variables["level"][:]

t925  =  t[:,3,:,:]
t_a   =  ma.zeros(t[:,4:,:,:].shape)
for ll in range(0,t_a.shape[1]):
    t_a[:,ll,:,:]  =  (t925 + t[:,ll+4,:,:])/2

disy,disx,location = cal_xydistance(lat,lon)

sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
ff = 2*omega*sinlat

r  = 8.314
constant1  =  r/ff
constant1[180]  =  1

#计算温度梯度
T_y  =  np.gradient(t_a,location,axis=2)
T_x  =  ma.zeros(T_y.shape)
for yy in range(0, t_a.shape[2]):
    T_x[:, :, yy, :] = np.gradient(t_a[:,:, yy, :], disx[yy], axis=2)

vt  =  ma.zeros(T_y.shape)
ut  = ma.zeros(T_y.shape)
for tt in range(0,61):
    for zz in range(0,38):
        for xx in range(0,576):
            vt[tt,zz,:,xx]  =  constant1*np.log(lev[3]/lev[zz+4])*T_x[tt,zz,:,xx]
            ut[tt,zz,:,xx]  =  -1*constant1*np.log(lev[3]/lev[zz+4])*T_y[tt,zz,:,xx]

time = np.arange(0,61)
a_v = {'longname': 'thermal_wind', 'units': 'm s-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
fout = create_nc_multiple('/data5/2019swh/data/', "thermal_wind_925hpa", time, lev[4:], lon, lat)
add_variables(fout, 'thermal_u', ut, a_v, 1)
add_variables(fout, 'thermal_v', vt, a_v, 1)
fout.close()

