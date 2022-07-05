'''
2020/12/17
merra2合成分析资料
利用KM Lau文献里面的公式计算DPV和MPV
'''
import os
import numpy as np
import Ngl, Nio
import json
from geopy.distance import distance
import numpy.ma as ma
import sys
import math
import copy
from netCDF4 import Dataset
sys.path.append("/data5/2019swh/mycode/module/")
from module_cal_heating import *
from module_writenc import *
from module_sun import *

f1 = Nio.open_file("/data5/2019swh/data/composite3.nc")
f2 = Nio.open_file("/data5/2019swh/data/potential_temperature.nc")
f3 = Nio.open_file("/data5/2019swh/data/composite_equivalent_tem.nc")
f4 = Nio.open_file("/data5/2019swh/data/ugvg.nc")

theate  = f2.variables["pt"][:]
theate_e = f3.variables["theate_e"][:]
u   =   f4.variables["ug"][:]
lon = f1.variables["lon"][:]
lat = f1.variables["lat"][:]
level = f1.variables["level"][:]
level *= 100

#uy = copy.deepcopy(u)

sinlat = np.array([]) #生成科里奥利力数组
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f = 2*omega*sinlat

disy,disx,location = cal_xydistance(lat,lon)

#theatep = copy.deepcopy(theate)
#theate_ep = copy.deepcopy(theate_e)

uy  =   np.gradient(u,location,axis=2)

for t in range(0,61):
    for lev in range(0,42):
        for y in range(0,361):
            uy[t,lev,y,:] = f[y] - uy[t,lev,y,:]



theatep = np.gradient(theate,level,axis=1)
theate_ep = np.gradient(theate_e, level, axis=1)

dpv = -9.8*uy*theatep
mpv = -9.8*uy*theate_ep
time = np.arange(61)+1
level /= 100
file = create_nc_multiple("/data5/2019swh/data/","dpv_mpv",time,level,lon,lat)
a_dpv   = {"longname":"dry_pv","units":"K m^2 kg-1 s-1","valid_range":[-1e+15,1e+15]}
a_mpv   = {"longname":"moist_pv","units":"K m^2 kg-1 s-1","valid_range":[-1e+15,1e+15]}
add_variables(file,"DPV",dpv,a_dpv,1)
add_variables(file,"MPV",mpv,a_mpv,1)

file.close()
