'''
2020/12/22
使用模式层的资料来计算PV
时间跨度4-6月
生成的层数：
'''

#先计算个例与生辰的进行比较
import os
import numpy as np
import Ngl, Nio
import json
from geopy.distance import distance
import numpy.ma as ma
import sys
import copy
import math
import numba
from numba import jit
from netCDF4 import Dataset
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *
a_pv   = {"longname":"potential vorticity","units":"K m+2 kg-1 s-1","valid_range":[0,100]}
path1 = '/data1/other_data/DataUpdate/ERA5/merra2/model_theta/'
path2 = '/data1/other_data/DataUpdate/ERA5/merra2/modelpv/'
file_theta = os.listdir(path1)
file_theta.sort()

#先计算水平与垂直距离
f1 = Nio.open_file(path1+file_theta[0])
time = f1.variables["time"][:]
lon  = f1.variables["lon"][:]
lat  = f1.variables["lat"][:]
lev = f1.variables["level"][:]
u = f1.variables["uwind"][:]
v = f1.variables["vwind"][:]
p    = f1.variables["PL"][:]
theta = f1.variables["theta"][:]


disy,disx,location = cal_xydistance(lat,lon)
sinlat = np.array([])
for ll in lat:
    sinlat = np.append(sinlat,math.sin(math.radians(ll)))
omega = 7.29e-5
f  =  2*omega*sinlat
corios = np.zeros((1,33,361,576))
for z in range(0,33):
    for x in range(0,576):
        corios[0,z,:,x] = f

def cal_modelpv(v,p,theta,u,f,disx,location):
    vp = copy.deepcopy(v)
    up = copy.deepcopy(v)
    thetap = copy.deepcopy(v)
    #计算垂直差分项
    for y in range(0,u.shape[2]):
        for x in range(0,u.shape[3]):
            vp[0,:,y,x] = np.gradient(v[0,:,y,x],p[0,:,y,x],axis=0)
            up[0, :, y, x] = np.gradient(u[0, :, y, x], p[0, :, y, x], axis=0)
            thetap[0, :, y, x] = np.gradient(theta[0, :, y, x], p[0, :, y, x], axis=0)

    #计算水平差分项
    vx = copy.deepcopy(v)
    thetax = copy.deepcopy(v)
    uy  =   np.gradient(u,location,axis=2)
    thetay  =   np.gradient(theta,location,axis=2)
    for latt in range(1, len(lat) - 1):
        thetax[0,:,latt,:] = np.gradient(theta[0,:,latt,:],disx[latt],axis=1)
        vx[0,:,latt,:] = np.gradient(v[0,:,latt,:],disx[latt],axis=1)

    pvh = (vp*thetax-up*thetay)*9.8

    pvv = -((f+vx-uy))*thetap*9.8

    all_pv = pvh+pvv
    return pvh,pvv,all_pv

for ff in file_theta:
    ff1 = Nio.open_file(path1 + ff)
    u = ff1.variables["uwind"][:]
    v = ff1.variables["vwind"][:]
    p = ff1.variables["PL"][:]
    theta = ff1.variables["theta"][:]
    pvh, pvv, all_pv = cal_modelpv(v, p, theta, u, corios, disx, location)
    time = np.arange(0, 1) + 1
    file = create_nc_multiple(path2, "model_pv2_" + ff[12:20], time, lev, lon, lat)
    add_variables(file, "pvh", pvh, a_pv, 1)
    add_variables(file, "pvv", pvv, a_pv, 1)
    add_variables(file, "all_pv", all_pv, a_pv, 1)

    file.close()