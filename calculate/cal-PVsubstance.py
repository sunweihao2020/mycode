'''
2020/1/7
使用先前计算的三维涡度计算位涡密度通量等物理量
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
from attribute import *

f2 = Nio.open_file("/data5/2019swh/data/three-dimension-vorticity.nc")
v_x = f2.variables["x-vorticity"][:]
v_y = f2.variables["y-vorticity"][:]
v_z = f2.variables["z-vorticity"][:]
time = f2.variables["time"][:]
lon  = f2.variables["lon"][:]
lat  = f2.variables["lat"][:]
level = f2.variables["level"][:]
f3 = Nio.open_file("/data5/2019swh/data/composite-modeltheta.nc")
theta = f3.variables["theta"][:]
f4 = Nio.open_file("/data5/2019swh/data/composite-model.nc")
h = f4.variables["H"][:]

jx = -1*np.gradient((v_x*theta),time,axis=0)
jy = -1*np.gradient((v_y*theta),time,axis=0)
jz = -1*np.gradient((v_z*theta),time,axis=0)
'''
disy,disx,location = cal_xydistance(lat,lon)

jyy = np.gradient(jy,location,axis=2)
jxx = np.zeros((61,33,361,576))
for i in range(1,360):
    jxx[:,:,i,:] = np.gradient(jx[:,:,i,:],disx[i],axis=2)

jzz = np.zeros((61,33,361,576))
for t in range(0,61):
    for y in range(0,361):
        for x in range(0,576):
            jzz[t,:,y,x] = np.gradient(jz[t,:,y,x],h[t,:,y,x],axis=0)

pW_pt = -1*(jyy+jzz+jxx)

fout = create_nc_multiple('/data5/2019swh/data/','W_change_with_t',time,level,lon,lat)
a_vorticity = {'longname': 'pvd','units': 'K m-1 s-1 day-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'Wt',pW_pt,a_vorticity,1)
add_variables(fout,'Wtx',-1*jxx,a_vorticity,1)
add_variables(fout,'Wty',-1*jyy,a_vorticity,1)



fout.close()
'''
fout = create_nc_multiple('/data5/2019swh/data/','J-3d',time,level,lon,lat)
a_vorticity = {'longname': 'PVS flux','units': 'K s-1','valid_range': [-1000000000000000.0, 1000000000000000.0]}
add_variables(fout,'jx',jx,a_vorticity,1)
add_variables(fout,'jy',jy,a_vorticity,1)
add_variables(fout,'jz',jz,a_vorticity,1)



fout.close()
