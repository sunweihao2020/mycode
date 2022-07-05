import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import math
sys.path.append("/mycode/module/")
from module_writenc import *
from module_sun import *
f1 = Nio.open_file("/data/div_vor.nc")
f2 = Nio.open_file("/data/composite3.nc")
u = f2.variables["uwind"][:]
v = f2.variables["vwind"][:]
lev = f2.variables["level"][:]
lon = f2.variables["lon"][:]
lat = f2.variables["lat"][:]
disy,disx,location = cal_xydistance(lat,lon)
vor = f1.variables["vor"][:]

vorx = ma.zeros((61,42,361,576))
vory = ma.zeros((61,42,361,576))

for t in range(0,u.shape[0]):
    for z in range(0,u.shape[1]):
        vory[t,z,:,:] = np.gradient(vor[t,z,:,:],location,axis=0)
        for latt in range(1,u.shape[2]-1):
            vorx[t,z,latt,:] = np.gradient(vor[t,z,latt,:],disx[latt],axis=0)
            
uvorx = u*vorx
vvory = v*vory

time = np.arange(0,61)
fout = create_nc_multiple('/data/','composite-divvor',time,lev,lon,lat)
a_w = {'longname': 'wind * vor gradient', 'units': '1', 'valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'v vor_gradient',vvory,a_w,1)
add_variables(fout,'u vor_gradient',uvorx,a_w,1)


fout.close()