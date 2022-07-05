'''
2021/2/27
本代码计算水汽输送以及水汽输送辐合辐散
注：比湿的单位是kg/kg
使用资料：/data/composite_specific_humidity.nc
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
sys.path.append("/data5/2019swh/mycode/module/")
from module_writenc import *
from module_sun import *
from attribute import *
f1 = Nio.open_file("/data5/2019swh/data/composite_specific_humidity.nc")
f2 = Nio.open_file("/data5/2019swh/data/composite3.nc")

q = f1.variables["specific_humidity"][:]
u = f2.variables["uwind"][:]
v = f2.variables["vwind"][:]
uq = u*q
vq = v*q
lon = f2.variables["lon"][:]
lat = f2.variables["lat"][:]
disy,disx,location = cal_xydistance(lat,lon)
ux = ma.zeros((61,42,361,576))
vy = ma.zeros((61,42,361,576))
for t in range(0,u.shape[0]):
    for z in range(0,u.shape[1]):
        vy[t,z,:,:] = np.gradient(v[t,z,:,:],location,axis=0)
        for latt in range(1,u.shape[2]-1):
            ux[t,z,latt,:] = np.gradient(u[t,z,latt,:],disx[latt],axis=0)
uxq = ux*q
vyq = vy*q

a_vq = {'longname': 'vapor transmission', 'units': 'm kg s-1 kg-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
a_vyq = {'longname': 'vapor transmission divergence', 'units': 'kg s-1 kg-1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}

lev = f2.variables["level"][:]
lat = f2.variables["lat"][:]
lon = f2.variables["lon"][:]
time = np.arange(0,61)
fout = create_nc_multiple('/data5/2019swh/data/','water_transmission',time,lev,lon,lat)
add_variables(fout,'uq',uq,a_vq,1)
add_variables(fout,'vq',vq,a_vq,1)
add_variables(fout,'uxq',uxq,a_vyq,1)
add_variables(fout,'vyq',vyq,a_vyq,1)

fout.close()