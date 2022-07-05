'''
2021/3/11
本代码计算爆发前夕赤道地区的受力情况，方程为简单的力学方程
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

f1 = Nio.open_file("/data5/2019swh/data/composite3.nc")
time  = f1.variables["time"][:]
h = f1.variables["H"][:]
h = h*9.8
v = f1.variables["vwind"][:]
lat = f1.variables["lat"][:]
lon = f1.variables["lon"][:]
lev = f1.variables["level"][:]

disy,disx,location = cal_xydistance(lat[180:],lon)
disy,disx,s = cal_xydistance(lat,lon)

h_x = ma.zeros(h.shape)
for t in range(0,h.shape[0]):
    for z in range(0,h.shape[1]):
        for latt in range(1,len(lat)-1):
            h_x[t,z,latt,:] = np.gradient(h[t,z,latt,:],disx[latt],axis=0)

coslat = np.array([])
for ll in lat[180:]:
    coslat = np.append(coslat,math.cos(math.radians(ll)))
omega = 7.29e-5
beta  =  2*omega*coslat


betay1 = beta*location
betay2 = -1*betay1
betay = np.zeros(361)
betay[181:] = betay1[1:]
betay[0:181] = betay2[::-1]

term2 = ma.zeros(h.shape)
for t in range(0,v.shape[0]):
    for z in range(0,v.shape[1]):
        for latt in range(0,v.shape[2]):
            term2[t,z,latt,:] = betay[latt] * v[t,z,latt,:] * -1

time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','composite-force-analysis',time,lev,lon,lat)
a_final = {'longname': 'force','units': 'm s-2','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'geopotential_force',h_x,a_final,1)
add_variables(fout,'beta_y_v',term2,a_final,1)
add_variables(fout,'pu_pt',(h_x+term2),a_final,1)
fout.close()