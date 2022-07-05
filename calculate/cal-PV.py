'''2020/11/24
merra2合成资料
计算PV用来诊断对称不稳定
'''
import os
import numpy as np
import Ngl, Nio
import numpy.ma as ma
from geopy.distance import distance
import sys
from netCDF4 import Dataset
import math
import copy
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
#from attribute import *

f1 = Nio.open_file("/data5/2019swh/data/composite3.nc")
f2 = Nio.open_file("/data5/2019swh/data/potential_temperature.nc")
ug = f1.variables["uwind"][:]
pt = f2.variables["pt"][:]
lat = f1.variables["lat"][:]
lon = f1.variables["lon"][:]
time = f1.variables["time"][:]
level = f1.variables["level"][:]
disy,disx,location = cal_xydistance(lat,lon)
gradient = np.zeros((61,42,361,576))
gradient = ma.array(gradient,mask=ug.mask)
gradient2 = copy.deepcopy(gradient)
gradient3 = copy.deepcopy(gradient)
gradient_x = copy.deepcopy(pt)
gradient_y = copy.deepcopy(pt)

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

for t in range(0,61):
    for lev in range(0,42):
        gradient3[t,lev,:,:] = np.gradient(ug[t,lev,:,:],location,axis=0)  #至此计算了偏ug偏y

ita = ma.array(ma.zeros((61,42,361,576)),mask=ug.mask)
for t in range(0,61):
    for lev in range(0,42):
        for yyyy in range(0,361):
            ita[t,lev,yyyy,:] = f[yyyy]-gradient3[t,lev,yyyy,:]  #绝对涡度

for t in range(0,61):
    for lev in range(0,42):
        gradient_y[t,lev,:,:] = np.gradient(pt[t,lev,:,:],location,axis=0)
        for latt in range(1, len(lat) - 1):
            gradient_x[t, lev, latt, :] = np.gradient(pt[t, lev, latt, :], disx[latt], axis=0)

quan_gradient = gradient_x + gradient_y

g = 9.8

final = g * ita * quan_gradient

a_ps    = {"longname":"PVG","units":"m2s-1Kkg-1","valid_range":[-1e+15,1e+15]}
file = create_nc("/data5/2019swh/data/","pvg1",time,level,lon,lat)
add_variables(file,"pvg",final,a_ps)
file.close()